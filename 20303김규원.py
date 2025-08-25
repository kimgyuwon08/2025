import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="📚 시험 공부 스케줄러", layout="wide")

# ---------------------------
# 🎨 스타일 (CSS 커스터마이징)
# ---------------------------
st.markdown("""
    <style>
    .main-title {
        font-size: 36px !important;
        font-weight: bold;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-title {
        font-size: 20px !important;
        font-weight: bold;
        margin-top: 20px;
        color: #333;
    }
    .calendar-table {
        border-collapse: collapse;
        width: 100%;
    }
    .calendar-table th, .calendar-table td {
        border: 1px solid #ddd;
        text-align: center;
        padding: 8px;
        vertical-align: top;
    }
    .calendar-table th {
        background-color: #f0f2f6;
        font-weight: bold;
    }
    .subject-box {
        display: inline-block;
        border-radius: 6px;
        padding: 2px 6px;
        margin: 2px;
        font-size: 12px;
        font-weight: bold;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>📚 시험 공부 스케줄 자동 생성기</div>", unsafe_allow_html=True)

# ---------------------------
# 📌 입력 영역
# ---------------------------
st.sidebar.header("⚙️ 설정")

exam_date = st.sidebar.date_input("시험 날짜 선택", min_value=datetime.today())
daily_study_hours = st.sidebar.slider("하루 공부 가능 시간 (시간)", 1, 12, 5)

st.sidebar.markdown("### 과목별 자신감/난이도 비율 (0~5)")
subjects = ["국어", "영어", "수학", "과학", "사회", 
            "생활과윤리", "한국지리", "생활과과학", "사회문제탐구"]

# 🎨 과목별 색상 매핑
subject_colors = {
    "국어": "#e74c3c",       # 빨강
    "영어": "#3498db",       # 파랑
    "수학": "#2ecc71",       # 초록
    "과학": "#9b59b6",       # 보라
    "사회": "#f39c12",       # 주황
    "생활과윤리": "#1abc9c",  # 청록
    "한국지리": "#e67e22",    # 진한 주황
    "생활과과학": "#34495e",  # 남색
    "사회문제탐구": "#d35400" # 갈색
}

weights = {}
for subj in subjects:
    weights[subj] = st.sidebar.slider(f"{subj}", 0, 5, 3)

# ---------------------------
# 📝 스케줄 계산
# ---------------------------
if st.sidebar.button("✏️ 스케줄 생성하기"):
    today = datetime.today().date()
    days_left = (exam_date - today).days

    if days_left <= 0:
        st.error("시험 날짜는 오늘 이후여야 합니다!")
    else:
        total_hours = days_left * daily_study_hours
        total_weight = sum(weights.values())

        study_plan = {}
        for subj, w in weights.items():
            if total_weight == 0:
                study_plan[subj] = 0
            else:
                study_plan[subj] = round(total_hours * (w / total_weight), 1)

        # ---------------------------
        # 📊 결과 출력
        # ---------------------------
        st.markdown("<div class='sub-title'>📌 과목별 총 공부 시간</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            df_plan = pd.DataFrame(list(study_plan.items()), columns=["과목", "총 공부 시간(h)"])
            st.dataframe(df_plan, use_container_width=True)

        with col2:
            st.bar_chart(df_plan.set_index("과목"))

        # ---------------------------
        # 📅 달력 기반 배정표
        # ---------------------------
        st.markdown("<div class='sub-title'>📅 달력 기반 공부 스케줄</div>", unsafe_allow_html=True)

        # 날짜별 빈 칸 만들기
        dates = [today + timedelta(days=i) for i in range(days_left)]
        daily_hours_left = {d: daily_study_hours for d in dates}

        # 공부 분배
        schedule = {d: [] for d in dates}
        for subj, total_h in study_plan.items():
            hours_left = total_h
            for d in dates:
                if hours_left <= 0:
                    break
                if daily_hours_left[d] > 0:
                    assign_h = min(1, hours_left, daily_hours_left[d])
                    schedule[d].append((subj, assign_h))
                    daily_hours_left[d] -= assign_h
                    hours_left -= assign_h

        # ---------------------------
        # 📅 달력 표시 (과목별 색상)
        # ---------------------------
        def make_calendar(schedule_dict):
            start_date = min(schedule_dict.keys())
            end_date = max(schedule_dict.keys())
            start_weekday = start_date.weekday()
            total_days = (end_date - start_date).days + 1

            html = "<table class='calendar-table'>"
            html += "<tr>" + "".join([f"<th>{day}</th>" for day in ["월","화","수","목","금","토","일"]]) + "</tr><tr>"

            # 빈 칸 채우기
            for _ in range(start_weekday):
                html += "<td></td>"

            for i in range(total_days):
                date = start_date + timedelta(days=i)
                day_num = date.day
                cell_html = f"<b>{day_num}</b><br>"
                for subj, h in schedule_dict[date]:
                    color = subject_colors.get(subj, "#95a5a6")
                    cell_html += f"<div class='subject-box' style='background:{color}'>{subj} {h}h</div><br>"
                html += f"<td>{cell_html}</td>"

                if (start_weekday + i + 1) % 7 == 0:
                    html += "</tr><tr>"

            html += "</tr></table>"
            return html

        st.markdown(make_calendar(schedule), unsafe_allow_html=True)

        st.success("✅ 스케줄이 성공적으로 생성되었습니다!")
