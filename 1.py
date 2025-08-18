import streamlit as st
import datetime
import random

# ------------------------------
# 간단한 운세/사주 생성 로직
# ------------------------------
def generate_fortune(name, birthdate):
    random.seed(str(name) + str(birthdate))

    love_fortune = random.choice([
        "💖 좋은 인연이 다가올 조짐이 보여요!",
        "💌 기존의 관계가 더 깊어질 운세예요!",
        "🌸 새로운 만남보다는 혼자만의 시간을 즐기면 좋아요!",
        "🔮 과거의 인연이 다시 다가올 수 있어요!"
    ])

    job_fortune = random.choice([
        "💼 새로운 기회가 열릴 운세예요!",
        "📈 꾸준한 노력이 인정받는 한 해가 될 거예요!",
        "📚 도전에 조심해야 하지만 배움의 기회가 있어요!",
        "🤝 협력과 팀워크가 중요한 시기예요!"
    ])

    life_advice = random.choice([
        "🍀 긍정적인 마음가짐이 행운을 부를 거예요!",
        "🌿 조금 더 주변을 돌아보면 좋은 기운이 찾아올 거예요!",
        "🚀 계획을 세우고 차근차근 나아가면 큰 성과를 얻을 거예요!",
        "🌙 감정의 기복을 잘 다스리면 좋은 결과가 있을 거예요!"
    ])

    return love_fortune, job_fortune, life_advice


# ------------------------------
# Streamlit 앱 UI
# ------------------------------
st.set_page_config(page_title="사주 & 운세 웹", page_icon="🔮", layout="centered")

# CSS로 디자인 커스터마이징
st.markdown("""
    <style>
        .main {
            background-color: #FFF5F7;
        }
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

# 사용자 입력
name = st.text_input("이름을 입력하세요:")
birthdate = st.date_input("생년월일을 선택하세요:", datetime.date(2000, 1, 1))

if st.button("✨ 운세 보기 ✨"):
    if name.strip() == "":
        st.warning("이름을 입력해주세요!")
    else:
        love, job, advice = generate_fortune(name, birthdate)

        # 카드 형태로 출력
        st.markdown(f"""
            <div class="card">
                <div class="subtitle">✨ {name}님의 운세 ✨</div>
                <div class="fortune-text"><b>💖 연애운:</b> {love}</div>
                <div class="fortune-text"><b>💼 직업운:</b> {job}</div>
                <div class="fortune-text"><b>🌟 오늘의 조언:</b> {advice}</div>
            </div>
        """, unsafe_allow_html=True)
