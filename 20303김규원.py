import streamlit as st
import pandas as pd
import datetime
import calendar

# 페이지 설정
st.set_page_config(page_title="📚 자동 공부 스케줄러", layout="wide")

st.title("📅 시험 대비 공부 스케줄 자동 생성기")
st.write("시험 날짜와 과목별 난이도/자신감을 입력하면 자동으로 공부 일정을 만들어줍니다!")

# 시험 날짜 입력
exam_date = st.date_input("시험 날짜를 선택하세요", datetime.date.today() + datetime.timedelta(days=14))
today = datetime.date.today()
total_days = (exam_date - today).days

if total_days <= 0:
    st.error("시험 날짜는 오늘 이후여야 합니다!")
    st.stop()

st.success(f"시험까지 남은 기간: {total_days}일")

# 과목 목록
subjects = ["국어", "영어", "수학", "과학", "사회", "생활과윤리", "한국지리", "생활과과학", "사회문제탐구"]

st.subheader("과목별 난이도 / 자신감 입력 (1~5)")
st.write("👉 난이도는 높을수록 더 많은 시간을 배정, 자신감은 높을수록 적은 시간을 배정합니다.")

subject_settings = {}
cols = st.columns(3)
for i, subj in enumerate(subjects):
    with cols[i % 3]:
        diff = st.slider(f"{subj} 난이도", 1, 5, 3, key=f"diff_{subj}")
        conf = st.slider(f"{subj} 자신감", 1, 5, 3, key=f"conf_{subj}")
        subject_settings[subj] = {"난이도": diff, "자신감": conf}

# 하루 최대 공부 시간
daily_hours = st.slider("하루 최대 공부 가능 시간 (시간)", 1, 12, 6)

# 스케줄 생성 버튼
if st.button("📌 스케줄 생성하기"):
    weights = {}
    for subj, vals in subject_settings.items():
        weights[subj] = vals["난이도"] * (6 - vals["자신감"])  # 난이도↑, 자신감↓ → 가중치↑

    total_weight = sum(weights.values())
    total_study_hours = total_days * daily_hours

    schedule = []
    for subj, w in weights.items():
        subj_hours = total_study_hours * (w / total_weight)
        schedule.append({"subject": subj, "총 공부시간(h)": subj_hours})

    schedule_df = pd.DataFrame(schedule)

    st.subheader("📊 과목별 총 공부시간")
    st.dataframe(schedule_df.style.format({"총 공부시간(h)": "{:.1f}"}))

    # 캘린더 표시
    st.subheader("🗓️ 달력 공부 계획")

    subject_colors = {
        "국어": "#e74c3c", "영어": "#3498db", "수학": "#2ecc71",
        "과학": "#9b59b6", "사회": "#f1c40f", "생활과윤리": "#1abc9c",
        "한국지리": "#e67e22", "생활과과학": "#34495e", "사회문제탐구": "#d35400"
    }

    # 날짜별 분배
    day_plan = {today + datetime.timedelta(days=i): [] for i in range(total_days)}
    subj_dict = dict(zip(schedule_df["subject"], schedule_df["총 공부시간(h)"]))  # ✅ 딕셔너리 변환 방식 수정

    # 균등 분배
    while any(v > 0 for v in subj_dict.values()):
        for d in day_plan.keys():
            for subj in subj_dict:
                if subj_dict[subj] > 0:
                    alloc = min(1, subj_dict[subj])
                    subj_dict[subj] -= alloc
                    day_plan[d].append((subj, alloc))

    # 달력 출력
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(today.year, today.month)

    for week in month_days:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].empty()
            else:
                date = datetime.date(today.year, today.month, day)
                with cols[i]:
                    st.markdown(f"**{day}**")
                    if date in day_plan:
                        for subj, hrs in day_plan[date]:
                            st.markdown(
                                f"<div style='background-color:{subject_colors.get(subj, '#ccc')};"
                                f"padding:5px;border-radius:8px;margin:2px;text-align:center;color:white;'>"
                                f"{subj} {hrs:.1f}h</div>",  # ✅ 소숫점 한 자리만 표시
                                unsafe_allow_html=True
                            )
