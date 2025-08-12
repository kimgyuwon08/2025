# app.py
import streamlit as st

st.set_page_config(page_title="MBTI 궁합 추천", page_icon="💖", layout="centered")

# --- CSS for card styling ---
st.markdown(
    """
    <style>
    .page-title {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .title-emoji {
        font-size: 36px;
    }
    .main-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        margin-bottom: 18px;
    }
    .result-card {
        background: linear-gradient(180deg, #ffffff, #fbfbff);
        border-radius: 12px;
        padding: 14px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.04);
        margin-top: 12px;
    }
    .mbti-badge {
        display:inline-block;
        padding:6px 10px;
        border-radius:8px;
        background: #f1f4ff;
        font-weight:700;
        margin-right:8px;
    }
    .match-item {
        display:flex;
        align-items:center;
        gap:8px;
        padding:6px 0;
    }
    .animal-img {
        border-radius:10px;
    }
    small { color: #555; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Header ---
st.markdown(
    """
    <div class="page-title">
      <div class="title-emoji">💖</div>
      <div>
        <h1 style="margin:0;">MBTI 궁합 추천</h1>
        <small>당신의 MBTI를 선택하면 궁합이 좋은 MBTI와 설명, 어울리는 동물 이미지를 보여드립니다.</small>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")  # spacing

mbti_types = ["ISTJ", "ISFJ", "INFJ", "INTJ",
              "ISTP", "ISFP", "INFP", "INTP",
              "ESTP", "ESFP", "ENFP", "ENTP",
              "ESTJ", "ESFJ", "ENFJ", "ENTJ"]

# MBTI 궁합 + 동물 이미지 (이미지 URL은 무료 이미지 출처 예시)
compatibility = {
    "ISTJ": {
        "궁합": ["ESFP", "ESTP"],
        "설명": "책임감 있고 성실한 ISTJ는 활발하고 유쾌한 ESFP, ESTP와 좋은 균형을 이룹니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/09/25/13/12/elephant-2785071_1280.jpg"
    },
    "ISFJ": {
        "궁합": ["ESFP", "ESTP"],
        "설명": "배려심 깊고 헌신적인 ISFJ는 사교적인 ESFP, ESTP와 잘 어울립니다.",
        "이미지": "https://cdn.pixabay.com/photo/2016/11/29/06/15/swan-1868697_1280.jpg"
    },
    "INFJ": {
        "궁합": ["ENFP", "ENTP"],
        "설명": "통찰력 있는 INFJ는 열정적인 ENFP, 창의적인 ENTP와 깊은 유대감을 형성합니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/01/20/00/30/wolf-1992716_1280.jpg"
    },
    "INTJ": {
        "궁합": ["ENFP", "ENTP"],
        "설명": "전략적이고 계획적인 INTJ는 자유롭고 창의적인 ENFP, ENTP와 서로를 보완합니다.",
        "이미지": "https://cdn.pixabay.com/photo/2016/02/19/10/00/owl-1206575_1280.jpg"
    },
    "ISTP": {
        "궁합": ["ESFJ", "ESTJ"],
        "설명": "차분하고 실용적인 ISTP는 조직적이고 사교적인 ESFJ, ESTJ와 좋은 파트너십을 가집니다.",
        "이미지": "https://cdn.pixabay.com/photo/2014/11/03/17/50/tiger-515037_1280.jpg"
    },
    "ISFP": {
        "궁합": ["ENFJ", "ESFJ"],
        "설명": "따뜻하고 온화한 ISFP는 활발하고 사람 중심적인 ENFJ, ESFJ와 잘 맞습니다.",
        "이미지": "https://cdn.pixabay.com/photo/2014/04/13/20/49/deer-323005_1280.jpg"
    },
    "INFP": {
        "궁합": ["ENFJ", "ENTJ"],
        "설명": "이상적이고 감성적인 INFP는 결단력 있는 ENFJ, ENTJ와 좋은 조화를 이룹니다.",
        "이미지": "https://cdn.pixabay.com/photo/2014/04/13/20/49/deer-323005_1280.jpg"
    },
    "INTP": {
        "궁합": ["ENTJ", "ESTJ"],
        "설명": "분석적이고 호기심 많은 INTP는 실행력이 강한 ENTJ, ESTJ와 시너지를 냅니다.",
        "이미지": "https://cdn.pixabay.com/photo/2014/11/11/14/50/cat-527124_1280.jpg"
    },
    "ESTP": {
        "궁합": ["ISFJ", "ISTJ"],
        "설명": "활동적이고 모험심 강한 ESTP는 안정적이고 신뢰할 수 있는 ISFJ, ISTJ와 잘 맞습니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/09/25/13/12/cheetah-2785071_1280.jpg"
    },
    "ESFP": {
        "궁합": ["ISFJ", "ISTJ"],
        "설명": "사교적이고 밝은 ESFP는 차분하고 헌신적인 ISFJ, ISTJ와 좋은 관계를 형성합니다.",
        "이미지": "https://cdn.pixabay.com/photo/2014/04/13/20/49/dolphin-323005_1280.jpg"
    },
    "ENFP": {
        "궁합": ["INFJ", "INTJ"],
        "설명": "에너지 넘치는 ENFP는 차분하고 깊이 있는 INFJ, INTJ와 좋은 시너지를 냅니다.",
        "이미지": "https://cdn.pixabay.com/photo/2014/04/13/20/49/parrot-323005_1280.jpg"
    },
    "ENTP": {
        "궁합": ["INFJ", "INTJ"],
        "설명": "도전적이고 창의적인 ENTP는 전략적인 INFJ, INTJ와 좋은 균형을 이룹니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/09/25/13/12/monkey-2785071_1280.jpg"
    },
    "ESTJ": {
        "궁합": ["ISTP", "INTP"],
        "설명": "체계적이고 리더십 있는 ESTJ는 유연하고 분석적인 ISTP, INTP와 잘 맞습니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/09/25/13/12/lion-2785071_1280.jpg"
    },
    "ESFJ": {
        "궁합": ["ISFP", "ISTP"],
        "설명": "따뜻하고 친절한 ESFJ는 차분하고 실용적인 ISFP, ISTP와 좋은 조화를 이룹니다.",
        "이미지": "https://cdn.pixabay.com/photo/2016/11/29/06/15/horse-1868697_1280.jpg"
    },
    "ENFJ": {
        "궁합": ["INFP", "ISFP"],
        "설명": "열정적이고 사람을 이끄는 ENFJ는 온화한 INFP, ISFP와 잘 맞습니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/09/25/13/12/dog-2785071_1280.jpg"
    },
    "ENTJ": {
        "궁합": ["INFP", "INTP"],
        "설명": "결단력 있고 목표 지향적인 ENTJ는 이상적인 INFP, 분석적인 INTP와 균형을 이룹니다.",
        "이미지": "https://cdn.pixabay.com/photo/2016/11/29/06/15/eagle-1868697_1280.jpg"
    }
}

# --- Sidebar or top selector ---
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("**당신의 MBTI를 선택하세요:**")
with col2:
    selected_mbti = st.selectbox("", mbti_types, index=mbti_types.index("INFP") if "INFP" in mbti_types else 0)

# --- Display main card with chosen MBTI ---
if selected_mbti in compatibility:
    data = compatibility[selected_mbti]
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    # top row: MBTI badge + title
    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px;">
            <div class="mbti-badge">{selected_mbti}</div>
            <div>
                <h2 style="margin:0;">{selected_mbti}와 잘 맞는 MBTI</h2>
                <small>아래 이미지는 이 MBTI를 상징하는 동물 이미지입니다.</small>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # content: image + description + matches
    left, right = st.columns([1, 2])
    with left:
        st.image(data["이미지"], use_column_width=True, caption=f"{selected_mbti}의 상징 동물", output_format="auto")
    with right:
        st.markdown(f"**설명:** {data['설명']}")
        st.markdown("**궁합 최고 MBTI:**")
        for match in data["궁합"]:
            st.markdown(f"<div class='match-item'>💞 <strong>{match}</strong></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # 하단: 각 추천 MBTI 카드 (작게)
    st.markdown("<div style='margin-top:10px;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-bottom:6px;'>추천 MBTI 상세</h4>", unsafe_allow_html=True)

    match_cols = st.columns(len(data["궁합"]))
    for i, match in enumerate(data["궁합"]):
        mdata = compatibility.get(match, None)
        with match_cols[i]:
            if mdata:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.image(mdata["이미지"], width=200)
                st.markdown(f"**{match}**")
                st.markdown(f"<small>{mdata['설명']}</small>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info(match)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.warning("아직 해당 MBTI의 궁합 데이터가 없습니다.")

# 작은 푸터
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<small>이미지 출처: Pixabay (무료 이미지 예시). 필요하면 다른 이미지로 교체해 드릴게요.</small>", unsafe_allow_html=True)
