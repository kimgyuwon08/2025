import streamlit as st
import datetime
import random

# --------------------------------
# 천간(10)과 지지(12)
# --------------------------------
heavenly_stems = ["갑(甲)", "을(乙)", "병(丙)", "정(丁)", "무(戊)", 
                  "기(己)", "경(庚)", "신(辛)", "임(壬)", "계(癸)"]

earthly_branches = ["자(子)", "축(丑)", "인(寅)", "묘(卯)", "진(辰)", "사(巳)",
                    "오(午)", "미(未)", "신(申)", "유(酉)", "술(戌)", "해(亥)"]

zodiac_animals = ["쥐🐭", "소🐂", "호랑이🐅", "토끼🐇", "용🐉", "뱀🐍",
                  "말🐎", "양🐑", "원숭이🐒", "닭🐓", "개🐕", "돼지🐖"]

elements = ["목(木) 🌳", "화(火) 🔥", "토(土) 🌍", "금(金) ⚔️", "수(水) 💧"]

# --------------------------------
# 사주 해석 함수
# --------------------------------
def get_four_pillars(birthdate, birthhour):
    # 연주
    year_stem = heavenly_stems[(birthdate.year - 4) % 10]
    year_branch = earthly_branches[(birthdate.year - 4) % 12]

    # 월주 (간단히 월 기준, 실제 계산은 더 복잡)
    month_stem = heavenly_stems[(birthdate.month + (birthdate.year % 10)) % 10]
    month_branch = earthly_branches[(birthdate.month + (birthdate.year % 12)) % 12]

    # 일주 (일수를 단순히 나눈 값)
    day_number = birthdate.toordinal()
    day_stem = heavenly_stems[day_number % 10]
    day_branch = earthly_branches[day_number % 12]

    # 시주 (2시간 단위 → 12지지)
    hour_branch = earthly_branches[(birthhour // 2) % 12]
    hour_stem = heavenly_stems[(birthhour // 2) % 10]

    return (year_stem, year_branch), (month_stem, month_branch), (day_stem, day_branch), (hour_stem, hour_branch)

def get_saju_explanation(stem, branch):
    explanations = {
        "갑(甲)": "나무처럼 곧고 강직한 성격이에요. 🌳",
        "을(乙)": "부드럽고 유연하며 배려심이 많아요. 🌱",
        "병(丙)": "태양처럼 밝고 에너지가 넘쳐요. ☀️",
        "정(丁)": "촛불처럼 따뜻하고 세심해요. 🕯️",
        "무(戊)": "든든하고 신뢰할 수 있는 성격이에요. 🪨",
        "기(己)": "차분하고 현실적인 성향이에요. 🌏",
        "경(庚)": "단단하고 결단력이 강해요. ⚔️",
        "신(辛)": "섬세하고 깔끔함을 중시해요. 💎",
        "임(壬)": "넓은 바다처럼 포용력이 있어요. 🌊",
        "계(癸)": "지혜롭고 직관력이 뛰어나요. 💧",
    }
    branch_ex = {
        "자(子)": "지혜롭고 재치 있는 성향.",
        "축(丑)": "끈기 있고 성실한 성향.",
        "인(寅)": "용감하고 리더십이 강한 성향.",
        "묘(卯)": "온화하고 예술적 감각이 뛰어남.",
        "진(辰)": "책임감 있고 현실적.",
        "사(巳)": "총명하고 호기심이 많음.",
        "오(午)": "열정적이고 활발함.",
        "미(未)": "온화하고 협력적.",
        "신(申)": "재주가 많고 활동적.",
        "유(酉)": "체계적이고 논리적.",
        "술(戌)": "정직하고 정의감이 강함.",
        "해(亥)": "감성적이고 직관력이 강함."
    }
    return explanations.get(stem, "") + " " + branch_ex.get(branch, "")

# --------------------------------
# 운세 생성
# --------------------------------
def generate_fortune(name, birthdate):
    random.seed(str(name) + str(birthdate))

    love = random.choice([
        "💖 좋은 인연이 다가올 조짐이 보여요!",
        "💌 오래된 인연이 새롭게 다가올 수 있어요.",
        "🌸 혼자만의 시간을 즐기면 운이 열려요.",
        "🔮 짝사랑이 현실이 될 수도 있어요!"
    ])
    job = random.choice([
        "💼 큰 기회가 다가오고 있어요!",
        "📈 노력의 결실을 맺을 시기예요.",
        "📚 새로운 배움이 필요한 시기예요.",
        "🤝 협력이 성과를 만드는 시기예요."
    ])
    money = random.choice([
        "💰 예상치 못한 수익이 생겨요!",
        "💸 지출이 많아질 수 있으니 조심!",
        "🏦 저축에 좋은 시기예요.",
        "🛍️ 소비를 줄이면 운이 더 좋아져요!"
    ])
    health = random.choice([
        "🌿 활력이 넘치는 시기예요!",
        "😴 피로가 쌓이지 않게 쉬어야 해요.",
        "💪 운동 시작에 좋은 시기예요.",
        "🍎 건강 관리가 중요한 시기예요."
    ])
    advice = random.choice([
        "🍀 긍정적인 마음가짐이 행운을 불러요!",
        "🌿 주변을 잘 살피면 기회가 와요.",
        "🚀 작은 시작이 큰 성과로 이어져요.",
        "🌙 마음의 평화를 찾으면 운이 밝아져요."
    ])
    return love, job, money, health, advice

# --------------------------------
# Streamlit UI
# --------------------------------
st.set_page_config(page_title="사주 & 운세", page_icon="🔮", layout="centered")

# CSS
st.markdown("""
    <style>
        .main { background-color: #FFF5F7; }
        .title { font-size: 2.2em; color: #FF6F91; text-align: center; font-weight: bold; }
        .card {
            background: #ffffff; padding: 20px; border-radius: 20px;
            box-shadow: 2px 4px 12px rgba(0,0,0,0.1); margin-top: 20px;
        }
        .subtitle { font-size: 1.3em; color: #6A0572; font-weight: bold; margin-bottom: 10px; }
        .fortune-text { font-size: 1.05em; color: #333333; margin: 8px 0; }
    </style>
""", unsafe_allow_html=True)

# 제목
st.markdown('<div class="title">🔮 디테일한 사주 & 운세 보기 🔮</div>', unsafe_allow_html=True)

# 입력
name = st.text_input("이름을 입력하세요:")
birthdate = st.date_input("생년월일을 선택하세요:", datetime.date(2000,1,1))
birthhour = st.slider("태어난 시간을 선택하세요 (0~23시)", 0, 23, 12)

if st.button("✨ 운세 보기 ✨"):
    if not name.strip():
        st.warning("이름을 입력해주세요!")
    else:
        # 사주팔자
        year, month, day, hour = get_four_pillars(birthdate, birthhour)

        # 해석
        year_ex = get_saju_explanation(*year)
        month_ex = get_saju_explanation(*month)
        day_ex = get_saju_explanation(*day)
        hour_ex = get_saju_explanation(*hour)

        # 운세
        love, job, money, health, advice = generate_fortune(name, birthdate)

        # 출력
        st.markdown(f"""
        <div class="card">
            <div class="subtitle">📜 {name}님의 사주팔자</div>
            <div class="fortune-text"><b>년주:</b> {year[0]} {year[1]} → {year_ex}</div>
            <div class="fortune-text"><b>월주:</b> {month[0]} {month[1]} → {month_ex}</div>
            <div class="fortune-text"><b>일주:</b> {day[0]} {day[1]} → {day_ex}</div>
            <div class="fortune-text"><b>시주:</b> {hour[0]} {hour[1]} → {hour_ex}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <div class="subtitle">✨ 오늘의 운세</div>
            <div class="fortune-text"><b>💖 연애운:</b> {love}</div>
            <div class="fortune-text"><b>💼 직업운:</b> {job}</div>
            <div class="fortune-text"><b>💰 금전운:</b> {money}</div>
            <div class="fortune-text"><b>🌿 건강운:</b> {health}</div>
            <div class="fortune-text"><b>🌟 오늘의 조언:</b> {advice}</div>
        </div>
        """, unsafe_allow_html=True)
