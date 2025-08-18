import streamlit as st
import datetime
import random

# ------------------------------
# 사주풀이 및 운세 생성 로직
# ------------------------------

def generate_saju(name, birthdate, birthtime=None):
    random.seed(str(name) + str(birthdate) + str(birthtime))

    # 오행 간단 계산 (랜덤 기반 시뮬레이션)
    elements = ["목(木)", "화(火)", "토(土)", "금(金)", "수(水)"]
    element_balance = {el: random.randint(1, 5) for el in elements}

    # 성향 설명 (간단 버전)
    character_desc = random.choice([
        "리더십이 강하고 주위 사람들을 이끄는 성향을 가지고 있어요.",
        "섬세하고 감수성이 풍부해 예술적 재능이 돋보여요.",
        "끈기와 성실함으로 꾸준히 성취하는 타입이에요.",
        "호기심이 많아 새로운 것에 도전하는 것을 좋아해요.",
        "사람들과 어울리기를 좋아하지만 혼자만의 시간도 중요시해요."
    ])

    # 각종 운세
    love_fortune = random.choice([
        "💖 올해는 좋은 인연이 다가올 조짐이 보여요!",
        "💌 연애보다는 자기계발에 더 집중하면 좋아요!",
        "🌸 오래 알고 지낸 사람 중에서 인연이 시작될 수 있어요!",
        "🔮 다가오는 계절에 설레는 만남이 있을 수 있어요!"
    ])

    job_fortune = random.choice([
        "💼 새로운 기회가 찾아와 성장할 수 있는 시기예요!",
        "📈 꾸준히 하던 일에서 인정을 받을 수 있어요!",
        "📚 도전이 필요하지만 성과가 크지 않을 수 있어요.",
        "🤝 협력과 팀워크가 중요한 시기예요!"
    ])

    money_fortune = random.choice([
        "💰 뜻밖의 재물이 들어올 수 있어요!",
        "🪙 씀씀이를 줄이는 것이 좋을 시기예요.",
        "🏦 투자보다는 저축이 더 유리해요.",
        "💎 주변 사람을 통해 금전적 기회가 찾아올 수 있어요!"
    ])

    health_fortune = random.choice([
        "🍀 건강운이 좋아 에너지가 넘쳐나요!",
        "😴 충분한 휴식이 필요해요.",
        "🥗 식습관 관리에 신경 쓰면 좋아요.",
        "🏃‍♂️ 운동을 꾸준히 하면 좋은 결과가 있어요!"
    ])

    relationship_fortune = random.choice([
        "👫 새로운 인맥이 생겨 삶에 활기를 불어넣을 거예요.",
        "🤗 가까운 사람과의 관계를 돌아보면 좋아요.",
        "💬 말실수에 주의하면 인간관계가 원만해져요.",
        "🎉 모임이나 행사에서 좋은 인연을 만날 수 있어요!"
    ])

    # 연애 시기 예측
    love_timing = random.choice([
        "다가오는 봄에 설레는 만남이 있을 수 있어요 🌸",
        "여름 무렵 뜨거운 인연이 찾아올 수 있어요 ☀️",
        "올해 말쯤 인연의 기운이 강해질 거예요 🎄",
        "내년 초에 진지한 만남이 다가올 수 있어요 🌟"
    ])

    # 해야 할 것 / 피해야 할 것
    do_good = random.choice([
        "📖 꾸준히 공부하거나 자기계발을 하면 운이 트여요.",
        "🤝 주변 사람들을 돕는 마음을 가지면 좋은 기운이 들어와요.",
        "🌿 자연과 가까이 지내면 마음이 안정되고 길운이 와요.",
        "🧘‍♀️ 차분히 계획을 세우고 실천하면 성과가 커져요."
    ])

    do_bad = random.choice([
        "⚡ 충동적인 결정은 피하는 게 좋아요.",
        "💸 큰 돈을 갑자기 쓰는 것은 좋지 않아요.",
        "🗣️ 불필요한 말로 오해를 사지 않도록 주의하세요.",
        "😴 게으름에 빠지면 기회를 놓칠 수 있어요."
    ])

    return {
        "element_balance": element_balance,
        "character_desc": character_desc,
        "love": love_fortune,
        "job": job_fortune,
        "money": money_fortune,
        "health": health_fortune,
        "relationship": relationship_fortune,
        "love_timing": love_timing,
        "do_good": do_good,
        "do_bad": do_bad
    }

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="정통 사주풀이", page_icon="📜", layout="centered")

st.markdown("""
    <style>
        .main { background-color: #FFFDF6; }
        .title {
            font-size: 2.5em;
            color: #C85C5C;
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
st.markdown('<div class="title">📜 정통 사주풀이 & 운세 📜</div>', unsafe_allow_html=True)

# 입력폼
name = st.text_input("이름을 입력하세요:")
birthdate = st.date_input("생년월일을 선택하세요:", datetime.date(2000, 1, 1))
birthtime = st.selectbox("태어난 시간을 선택하세요 (모르면 '모름' 선택)", 
                         ["모름", "자시(23~01시)", "축시(01~03시)", "인시(03~05시)", 
                          "묘시(05~07시)", "진시(07~09시)", "사시(09~11시)", 
                          "오시(11~13시)", "미시(13~15시)", "신시(15~17시)", 
                          "유시(17~19시)", "술시(19~21시)", "해시(21~23시)"])

if st.button("🔮 사주풀이 보기"):
    if name.strip() == "":
        st.warning("이름을 입력해주세요!")
    else:
        result = generate_saju(name, birthdate, birthtime)

        # 카드 레이아웃 출력
        st.markdown(f"""
            <div class="card">
                <div class="subtitle">✨ {name}님의 사주풀이 ✨</div>
                <div class="fortune-text"><b>🌟 성향:</b> {result['character_desc']}</div>
                <div class="fortune-text"><b>🌳 오행의 균형:</b> {result['element_balance']}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="card">
                <div class="subtitle">📌 운세 해석</div>
                <div class="fortune-text"><b>💖 연애운:</b> {result['love']}</div>
                <div class="fortune-text"><b>💼 직업운:</b> {result['job']}</div>
                <div class="fortune-text"><b>💰 재물운:</b> {result['money']}</div>
                <div class="fortune-text"><b>🍀 건강운:</b> {result['health']}</div>
                <div class="fortune-text"><b>🤝 인간관계운:</b> {result['relationship']}</div>
                <div class="fortune-text"><b>📅 연애 시기:</b> {result['love_timing']}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="card">
                <div class="subtitle">⚖️ 생활 조언</div>
                <div class="fortune-text"><b>✅ 하면 좋은 것:</b> {result['do_good']}</div>
                <div class="fortune-text"><b>❌ 피해야 할 것:</b> {result['do_bad']}</div>
            </div>
        """, unsafe_allow_html=True)
