# app.py
# -----------------------------
# Streamlit 공부 스케줄 자동 생성기
# - 시험 날짜까지 남은 기간에 맞춰 과목별 공부시간 분배
# - 난이도(높을수록 어려움) / 자신도(높을수록 자신있음) 가중치 반영
# - 평일/주말 가능 시간 및 제외 날짜 반영
# - 일자별 세부 타임블록 생성 + CSV/ICS 다운로드
# -----------------------------

import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

st.set_page_config(page_title="공부 스케줄 자동 생성기", page_icon="🗓️", layout="wide")

# -----------------------------
# 유틸 함수
# -----------------------------
def daterange(start: date, end: date):
    """end 포함 (시험일 포함)"""
    for n in range((end - start).days + 1):
        yield start + timedelta(n)

def nice_round_hours(x: float, step: float = 0.5):
    """0.5시간 단위 반올림"""
    return round(x / step) * step

def make_weights(df, alpha: float, beta: float, min_floor: float):
    """
    과목별 가중치 계산:
    - 난이도는 높을수록 더 많은 시간이 필요 → +alpha * difficulty
    - 자신도는 높을수록 적은 시간이 필요 → +beta * (6 - confidence)
    - 최소 바닥 가중치(min_floor) 보장
    """
    raw = alpha * df["난이도(1-5)"] + beta * (6 - df["자신도(1-5)"])
    w = raw.clip(lower=0) + min_floor
    return w

def split_total_hours_by_weights(total_hours: float, weights: np.ndarray, step: float = 0.5):
    """가중치 비율로 총 시간을 나누고 0.5h 단위로 반올림, 총합 보정"""
    if weights.sum() == 0:
        # 가중치가 0이면 균등 분배
        weights = np.ones_like(weights, dtype=float)
    ratio = weights / weights.sum()
    alloc = ratio * total_hours
    alloc = np.array([nice_round_hours(a, step) for a in alloc], dtype=float)
    # 반올림으로 생긴 오차 보정
    diff = round((total_hours - alloc.sum()) / step)
    # 남은 step 단위를 큰 가중치 순으로 더하기/빼기
    order = np.argsort(-weights)
    i = 0
    while diff != 0 and i < 10000:
        idx = order[abs(i) % len(order)]
        if diff > 0:
            alloc[idx] += step
            diff -= 1
        else:
            if alloc[idx] - step >= 0:
                alloc[idx] -= step
                diff += 1
        i += 1
    return alloc

def build_daily_capacity(start: date, end: date, weekday_hours: float, weekend_hours: float, excluded: set):
    """날짜별 가능 공부시간 (시간 단위)"""
    days = []
    for d in daterange(start, end):
        if d in excluded:
            hours = 0.0
        else:
            if d.weekday() < 5:
                hours = weekday_hours
            else:
                hours = weekend_hours
        days.append({"date": d, "capacity_h": max(0.0, hours)})
    return pd.DataFrame(days)

def allocate_to_days(subjects_df: pd.DataFrame,
                     per_subject_hours: np.ndarray,
                     daily_capacity_df: pd.DataFrame,
                     block_h: float = 1.0,
                     fill_mode: str = "proportional"):
    """
    과목별 총 시간(per_subject_hours)을 날짜별 capacity에 맞춰 블록 단위로 할당.
    fill_mode:
      - 'round_robin': 과목을 돌아가며 1블록씩 채움
      - 'proportional': 남은 시간 비율이 큰 과목에 우선 배정
    반환: schedule_df(date, subject, hours), daily_summary_df(date, total_hours)
    """
    # 준비
    subjects = subjects_df["과목"].tolist()
    remaining = {s: per_subject_hours[i] for i, s in enumerate(subjects)}
    schedule_rows = []

    # 날짜 반복
    for _, row in daily_capacity_df.iterrows():
        d = row["date"]
        remain_capacity = float(row["capacity_h"])
        if remain_capacity <= 0.0:
            continue

        # 하루 스케줄 채우기
        while remain_capacity >= block_h and sum(remaining.values()) > 0:
            # 다음 과목 선택
            if fill_mode == "round_robin":
                # 남은 과목 리스트(>0) 순환
                order = [s for s in subjects if remaining[s] > 0]
                if not order:
                    break
                pick = order[0]
                # 회전
                subjects = subjects[1:] + subjects[:1]
            else:  # proportional
                candidates = [(s, r) for s, r in remaining.items() if r > 0]
                if not candidates:
                    break
                # 남은 시간이 큰 과목 우선
                pick = sorted(candidates, key=lambda x: -x[1])[0][0]

            # 블록 배정
            block = min(block_h, remaining[pick], remain_capacity)
            block = nice_round_hours(block, 0.5)
            if block <= 0:
                break

            schedule_rows.append({"date": d, "과목": pick, "시간(h)": float(block)})
            remaining[pick] = round(remaining[pick] - block, 3)
            remain_capacity = round(remain_capacity - block, 3)

    schedule_df = pd.DataFrame(schedule_rows)
    if schedule_df.empty:
        return schedule_df, daily_capacity_df.rename(columns={"capacity_h": "배정가능시간(h)"}).assign(**{"배정총합(h)": 0.0})

    daily_summary = schedule_df.groupby("date", as_index=False)["시간(h)"].sum()
    daily_summary = daily_capacity_df.merge(daily_summary, on="date", how="left").fillna({"시간(h)": 0.0})
    daily_summary = daily_summary.rename(columns={"capacity_h": "배정가능시간(h)", "시간(h)": "배정총합(h)"})
    return schedule_df, daily_summary

def to_ics(schedule_df: pd.DataFrame, title_prefix="Study"):
    """단순한 iCalendar (.ics) 생성"""
    if schedule_df.empty:
        return "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//StudyScheduler//EN\nEND:VCALENDAR"

    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//StudyScheduler//EN"]
    base_start_hour = 18

    for d, df_day in schedule_df.groupby("date"):
        cursor = datetime(d.year, d.month, d.day, base_start_hour, 0)
        for _, r in df_day.iterrows():
            minutes = int(round(float(r["시간(h)"]) * 60))
            dtstart = cursor
            dtend = cursor + timedelta(minutes=minutes)
            cursor = dtend

            uid = f"{dtstart.strftime('%Y%m%dT%H%M%S')}@studyscheduler"
            lines += [
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
                f"DTSTART:{dtstart.strftime('%Y%m%dT%H%M%S')}",
                f"DTEND:{dtend.strftime('%Y%m%dT%H%M%S')}",
                f"SUMMARY:{title_prefix} - {r['과목']}",
                f"DESCRIPTION:{r['과목']} 공부 {r['시간(h)']}시간",
                "END:VEVENT",
            ]
    lines.append("END:VCALENDAR")
    return "\n".join(lines)

# -----------------------------
# 사이드바: 입력 폼
# -----------------------------
with st.sidebar:
    st.title("🛠️ 설정")
    st.caption("시험 날짜, 과목, 가중치, 가능 시간 등을 입력하세요.")

    today = date.today()
    exam_date = st.date_input("시험 날짜", value=today + timedelta(days=14), min_value=today)

    st.markdown("**1) 과목 목록 & 난이도/자신도**")
    st.caption("난이도: 어려울수록 5, 자신도: 자신있을수록 5")
    default_subjects = pd.DataFrame({
        "과목": ["국어", "수학", "영어", "과학", "사회"],
        "난이도(1-5)": [3, 4, 3, 4, 2],
        "자신도(1-5)": [3, 2, 3, 2, 4],
    })
    subjects_df = st.data_editor(
        default_subjects,
        use_container_width=True,
        num_rows="dynamic",
        key="subjects_editor",
    )

    st.markdown("**2) 가중치 파라미터**")
    alpha = st.slider("난이도 가중치 α", 0.0, 3.0, 1.0, 0.1)
    beta  = st.slider("자신도 역가중치 β (자신도 낮을수록 +)", 0.0, 3.0, 1.0, 0.1)
    min_floor = st.slider("최소 바닥 가중치", 0.0, 1.0, 0.2, 0.1)

    st.markdown("**3) 총 공부 시간 설정**")
    total_hours = st.number_input("총 공부 시간 (시간)", min_value=0.0, value=40.0, step=1.0)

    st.markdown("**4) 요일별 가능 시간**")
    weekday_hours = st.number_input("평일 1일 가능 시간 (시간)", min_value=0.0, value=2.0, step=0.5)
    weekend_hours = st.number_input("주말 1일 가능 시간 (시간)", min_value=0.0, value=4.0, step=0.5)

    st.markdown("**5) 제외 날짜**")
    excluded_dates = st.date_input("공부 불가 날짜(여러 날 선택)", [], min_value=today, max_value=exam_date)

    st.markdown("**6) 세부 옵션**")
    block_h = st.select_slider("세부 블록 길이", options=[0.5, 1.0, 1.5, 2.0], value=1.0)
    fill_mode = st.radio("할당 방식", ["proportional", "round_robin"], index=0,
                         captions=["남은시간 큰 과목 우선", "과목을 돌아가며 순차 할당"])

# -----------------------------
# 본문: 출력
# -----------------------------
st.title("🗓️ 공부 스케줄 자동 생성기")

colA, colB, colC = st.columns([1, 1, 1])
with colA:
    st.metric("오늘", date.today().strftime("%Y-%m-%d"))
with colB:
    st.metric("시험 날짜", exam_date.strftime("%Y-%m-%d"))
with colC:
    days_left = (exam_date - date.today()).days
    st.metric("남은 일수", f"{max(0, days_left)}일")

# 유효성 검사
if subjects_df.empty or subjects_df["과목"].isna().all():
    st.warning("과목을 최소 1개 이상 입력하세요.")
    st.stop()

for col in ["난이도(1-5)", "자신도(1-5)"]:
    subjects_df[col] = pd.to_numeric(subjects_df[col], errors="coerce").fillna(3).clip(1, 5).astype(int)

# 가중치 및 배분
weights = make_weights(subjects_df, alpha=alpha, beta=beta, min_floor=min_floor)
subjects_df = subjects_df.assign(가중치=np.round(weights, 3))

per_subject_hours = split_total_hours_by_weights(total_hours, weights.values, step=0.5)
subjects_df = subjects_df.assign(배정시간_h=np.round(per_subject_hours, 2))

st.subheader("📊 과목별 배정 결과")
st.dataframe(subjects_df, use_container_width=True)

# 날짜별 capacity
excluded_set = set(excluded_dates if isinstance(excluded_dates, list) else [excluded_dates])
daily_capacity_df = build_daily_capacity(date.today(), exam_date, weekday_hours, weekend_hours, excluded_set)

schedule_df, daily_summary_df = allocate_to_days(
    subjects_df, per_subject_hours, daily_capacity_df, block_h=float(block_h), fill_mode=fill_mode
)

st.subheader("🧩 일자별 요약")
st.dataframe(daily_summary_df, use_container_width=True)

st.subheader("📅 상세 스케줄")
if schedule_df.empty:
    st.info("생성된 스케줄이 없습니다.")
else:
    schedule_df = schedule_df.sort_values(["date", "과목"]).reset_index(drop=True)
    st.dataframe(schedule_df, use_container_width=True)

    pivot = schedule_df.pivot_table(index="date", columns="과목", values="시간(h)", aggfunc="sum", fill_value=0.0)
    st.dataframe(pivot, use_container_width=True)

    csv = schedule_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("CSV 다운로드", data=csv, file_name="study_schedule.csv", mime="text/csv")

    ics_text = to_ics(schedule_df, title_prefix="Study")
    st.download_button("ICS 다운로드", data=ics_text, file_name="study_schedule.ics", mime="text/calendar")
