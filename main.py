import streamlit as st

st.set_page_config(page_title="MBTI 궁합 추천", page_icon="💖", layout="centered")

st.title("💖 MBTI 궁합 추천")
st.write("당신의 MBTI를 선택하면 궁합이 좋은 MBTI와 설명, 이미지를 보여드립니다!")

mbti_types = ["ISTJ", "ISFJ", "INFJ", "INTJ",
              "ISTP", "ISFP", "INFP", "INTP",
              "ESTP", "ESFP", "ENFP", "ENTP",
              "ESTJ", "ESFJ", "ENFJ", "ENTJ"]

# MBTI 궁합 데이터 (16종 완성)
compatibility = {
    "ISTJ": {
        "궁합": ["ESFP", "ESTP"],
        "설명": "책임감 있고 성실한 ISTJ는 활발하고 유쾌한 ESFP, ESTP와 좋은 균형을 이룹니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/02/15/12/12/couple-2069051_1280.png"
    },
    "ISFJ": {
        "궁합": ["ESFP", "ESTP"],
        "설명": "배려심 깊고 헌신적인 ISFJ는 에너제틱하고 사교적인 ESFP, ESTP와 잘 어울립니다.",
        "이미지": "https://cdn.pixabay.com/photo/2016/03/31/20/12/couple-1296393_1280.png"
    },
    "INFJ": {
        "궁합": ["ENFP", "ENTP"],
        "설명": "통찰력 있는 INFJ는 열정적인 ENFP, 창의적인 ENTP와 깊은 유대감을 형성합니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/02/15/12/12/couple-2069051_1280.png"
    },
    "INTJ": {
        "궁합": ["ENFP", "ENTP"],
        "설명": "전략적이고 계획적인 INTJ는 자유롭고 창의적인 ENFP, ENTP와 서로를 보완합니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/01/31/17/44/couple-2022753_1280.png"
    },
    "ISTP": {
        "궁합": ["ESFJ", "ESTJ"],
        "설명": "차분하고 실용적인 ISTP는 조직적이고 사교적인 ESFJ, ESTJ와 좋은 파트너십을 가집니다.",
        "이미지": "https://cdn.pixabay.com/photo/2014/12/10/21/01/love-563730_1280.png"
    },
    "ISFP": {
        "궁합": ["ENFJ", "ESFJ"],
        "설명": "따뜻하고 온화한 ISFP는 활발하고 사람 중심적인 ENFJ, ESFJ와 잘 맞습니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/02/15/12/12/couple-2069051_1280.png"
    },
    "INFP": {
        "궁합": ["ENFJ", "ENTJ"],
        "설명": "이상적이고 감성적인 INFP는 결단력 있는 ENFJ, ENTJ와 좋은 조화를 이룹니다.",
        "이미지": "https://cdn.pixabay.com/photo/2014/12/10/21/01/love-563730_1280.png"
    },
    "INTP": {
        "궁합": ["ENTJ", "ESTJ"],
        "설명": "분석적이고 호기심 많은 INTP는 실행력이 강한 ENTJ, ESTJ와 시너지를 냅니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/01/31/17/44/couple-2022753_1280.png"
    },
    "ESTP": {
        "궁합": ["ISFJ", "ISTJ"],
        "설명": "활동적이고 모험심 강한 ESTP는 안정적이고 신뢰할 수 있는 ISFJ, ISTJ와 잘 맞습니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/08/06/11/29/people-2594324_1280.jpg"
    },
    "ESFP": {
        "궁합": ["ISFJ", "ISTJ"],
        "설명": "사교적이고 밝은 ESFP는 차분하고 헌신적인 ISFJ, ISTJ와 좋은 관계를 형성합니다.",
        "이미지": "https://cdn.pixabay.com/photo/2016/03/31/20/12/couple-1296393_1280.png"
    },
    "ENFP": {
        "궁합": ["INFJ", "INTJ"],
        "설명": "에너지 넘치는 ENFP는 차분하고 깊이 있는 INFJ, INTJ와 좋은 시너지를 냅니다.",
        "이미지": "https://cdn.pixabay.com/photo/2014/12/10/21/01/love-563730_1280.png"
    },
    "ENTP": {
        "궁합": ["INFJ", "INTJ"],
        "설명": "도전적이고 창의적인 ENTP는 전략적인 INFJ, INTJ와 좋은 균형을 이룹니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/08/06/11/29/people-2594324_1280.jpg"
    },
    "ESTJ": {
        "궁합": ["ISTP", "INTP"],
        "설명": "체계적이고 리더십 있는 ESTJ는 유연하고 분석적인 ISTP, INTP와 잘 맞습니다.",
        "이미지": "https://cdn.pixabay.com/photo/2016/03/31/20/12/couple-1296393_1280.png"
    },
    "ESFJ": {
        "궁합": ["ISFP", "ISTP"],
        "설명": "따뜻하고 친절한 ESFJ는 차분하고 실용적인 ISFP, ISTP와 좋은 조화를 이룹니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/02/15/12/12/couple-2069051_1280.png"
    },
    "ENFJ": {
        "궁합": ["INFP", "ISFP"],
        "설명": "열정적이고 사람을 이끄는 ENFJ는 온화한 INFP, ISFP와 좋은 관계를 유지합니다.",
        "이미지": "https://cdn.pixabay.com/photo/2014/12/10/21/01/love-563730_1280.png"
    },
    "ENTJ": {
        "궁합": ["INFP", "INTP"],
        "설명": "결단력 있고 목표 지향적인 ENTJ는 이상적인 INFP, 분석적인 INTP와 균형을 이룹니다.",
        "이미지": "https://cdn.pixabay.com/photo/2017/01/31/17/44/couple-2022753_1280.png"
    }
}

# MBTI 선택
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요:", mbti_types)

# 결과 출력
if selected_mbti in compatibility:
    data = compatibility[selected_mbti]
    st.subheader(f"💌 {selected_mbti}와 잘 맞는 MBTI")
    st.image(data["이미지"], width=300)
    st.markdown(f"**설명:** {data['설명']}")
    st.markdown("**궁합 최고 MBTI:**")
    for match in data["궁합"]:
        st.markdown(f"- 💕 **{match}**")
else:
    st.warning("아직 해당 MBTI의 궁합 데이터가 없습니다.")
