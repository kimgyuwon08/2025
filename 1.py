import streamlit as st
import datetime
import random

# ------------------------------
# 사주 기본 성향 해석
# ------------------------------
def get_saju_description(year, month, day):
    zodiac = [
        "쥐띠 🐭 - 총명하고 재치 있는 성향!",
        "소띠 🐮 - 성실하고 끈기 있는 성향!",
        "호랑이띠 🐯 - 용감하고 추진력이 강한 성향!",
        "토끼띠 🐰 - 온화하고 다정한 성향!",
        "용띠 🐲 - 카리스마와 리더십이 돋보이는 성향!",
        "뱀띠 🐍 - 지혜롭고 분석적인 성향!",
        "말띠 🐴 - 활발하고 자유로운 성향!",
        "양띠 🐑 - 따뜻하고 배려심 많은 성향!",
        "원숭이띠 🐵 - 재주 많고 유머러스한 성향!",
        "닭띠 🐔 - 꼼꼼하고 성실한 성향!",
        "개띠 🐶 - 의리 있고 정직한 성향!",
        "돼지띠 🐷 - 너그럽고 긍정적인 성향!"
    ]
    zodiac_index = (year - 4) % 12
    return zodiac[zodiac_index]


# ------------------------------
# 운세 생성
# ------------------------------
def generate_fortunes(name, birthdate, birthtime=None):
    random.seed(str(name) + str(birthdate) + str(birthtime))

    love_fortune = random.choice([
        "💖 설레는 인연이 다가올 조짐!",
        "🌸 기존의 관계가 더 깊어질 운세!",
        "💌 혼자만의 시간이 필요하지만, 곧 기회가 찾아올 거예요!",
        "🔮 과거의 인연이 다시 다가올 수 있어요!"
    ])

    job_fortune = random.choice([
        "💼 새로운 기회가 열릴 운세!",
        "📈 꾸준한 노력이 빛을 발하는 시기!",
        "📚 배움이 곧 성장으로 이어질 거예요!",
        "🤝 협력과 네트워크가 중요한 시기!"
    ])

    money_fortune = random.choice([
        "💰 재물이 모이고 운이 상승해요!",
        "🪙 작은 투자에 신중해야 해요!",
        "🍀 뜻밖의 행운이 재정에 도움을 줘요!",
        "📉 소비를 조심해야 하는 시기예요!"
    ])

    health_fortune = random.choice([
        "💪 활력이 넘치는 하루!",
        "🧘‍♀️ 균형 있는 생활이 필요해요!",
        "🌿 스트레스 조절이 중요해요!",
        "😴 충분한 휴식이 필요할 때예요!"
    ])

    advice = random.choice([
        "🍀 긍정적인 태도가 행운을 불러올 거예요!",
        "🌙 감정의 균형을 잘 잡으면 좋은 일이 생겨요!",
        "🚀 도전의 시도를 두려워하지 마세요!",
        "🌿 주변 사람과의 유대가 복을 가져와요!"
    ])

    # 연애 시기 예측
    love_timing = random.choice([
        "📅 앞으로 3개월 이내에 새로운 인연이 다가올 수 있어요!",
        "📅 올해 가을쯤 설레는 만남이 예상돼요!",
        "📅 내년 초, 뜻밖의 인연이 찾아올 거예요!",
        "📅 아직은 스스로를 가꾸는 시간이 필요해요. 1~2년 뒤 좋은 인연이 다가와요!"
    ])

    return love_fortune, job_fortune, money_fortune, health_fortune, advice, love_timing


# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="사주 & 운세 웹", page_icon="🔮", layout="centered")

# CSS 꾸미기
st.markdown("""
    <style>
        .main { background-color: #FFF5F7; }
        .title {
            font-size: 2.2em;
            color: #FF6F91;
            text-align: center;
            font-weight: bold;
        }
        .card {
            background: #ffffff;
            padding: 20px;
            border-radius: 20px;
            box-shadow: 2px 4px 12px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        .subtitle {
            font-size: 1.4em;
            color: #6A0572;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .fortune-text {
            font-size: 1.1em;
            color: #333333;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# 제목
st.markdown('<div class="title">🔮 나의 사주 & 운세 보기 🔮</div>', unsafe_allow_html=True)

# 입력값
name = st.text_input("이름을 입력하세요:")
birthdate = st.date_input("생년월일을 선택하세요:", datetime.date(2000, 1, 1))
birthtime_option = st.selectbox("태어난 시간을 선택하세요 (모르면 '모름' 선택)", 
                                ["모름", "자시(23~1시)", "축시(1~3시)", "인시(3~5시)", "묘시(5~7시)", 
                                 "진시(7~9시)", "사시(9~11시)", "오시(11~13시)", "미시(13~15시)", 
                                 "신시(15~17시)", "유시(17~19시)", "술시(19~21시)", "해시(21~23시)"])

if st.button("✨ 운세 보기 ✨"):
    if name.strip() == "":
        st.warning("이름을 입력해주세요!")
    else:
        # 사주 설명
        saju = get_saju_description(birthdate.year, birthdate.month, birthdate.day)
        love, job, money, health, advice, love_timing = generate_fortunes(name, birthdate, birthtime_option)

        st.markdown(f"""
            <div class="card">
                <div class="subtitle">🌟 {name}님의 사주 기본 성향</div>
                <div class="fortune-text">{saju}</div>
            </div>

            <div class="card">
                <div class="subtitle">✨ 오늘의 운세 ✨</div>
                <div class="fortune-text"><b>💖 연애운:</b> {love}</div>
                <div class="fortune-text"><b>💼 직업운:</b> {job}</div>
                <div class="fortune-text"><b>💰 재물운:</b> {money}</div>
                <div class="fortune-text"><b>🩺 건강운:</b> {health}</div>
                <div class="fortune-text"><b>💌 연애 시기 예측:</b> {love_timing}</div>
                <div class="fortune-text"><b>🌟 오늘의 조언:</b> {advice}</div>
            </div>
        """, unsafe_allow_html=True)
