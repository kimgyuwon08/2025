import streamlit as st

# MBTI별 궁합 + 설명 + 동물 이미지
mbti_data = {
    "INFP": {
        "match": ["ENFJ", "ENTJ"],
        "desc": "이상적이고 감성적인 INFP는 결단력 있는 ENFJ, ENTJ와 좋은 조화를 이룹니다.",
        "image": "https://images.unsplash.com/photo-1501706362039-c6e08e1e1f06"  # 사슴
    },
    "ENFP": {
        "match": ["INFJ", "INTJ"],
        "desc": "에너지가 넘치고 창의적인 ENFP는 깊이 있는 INFJ, INTJ와 좋은 궁합을 가집니다.",
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"  # 돌고래
    },
    "ENTJ": {
        "match": ["INFP", "INTP"],
        "desc": "리더십과 추진력이 강한 ENTJ는 차분한 INFP, 분석적인 INTP와 잘 어울립니다.",
        "image": "https://images.unsplash.com/photo-1552410260-0fc8d0b24f7c"  # 사자
    },
    "INTP": {
        "match": ["ENTJ", "ESTJ"],
        "desc": "논리적이고 창의적인 INTP는 결단력 있는 ENTJ, ESTJ와 좋은 관계를 맺습니다.",
        "image": "https://images.unsplash.com/photo-1561948955-570b270e7c36"  # 올빼미
    },
    "INFJ": {
        "match": ["ENFP", "ENTP"],
        "desc": "통찰력 있고 따뜻한 INFJ는 활발한 ENFP, ENTP와 잘 어울립니다.",
        "image": "https://images.unsplash.com/photo-1561948954-4b22b62b196a"  # 백호
    },
    "ENTP": {
        "match": ["INFJ", "INTJ"],
        "desc": "아이디어가 넘치는 ENTP는 깊이 있는 INFJ, INTJ와 조화를 이룹니다.",
        "image": "https://images.unsplash.com/photo-1546182990-dffeafbe841d"  # 원숭이
    },
    "INTJ": {
        "match": ["ENFP", "ENTP"],
        "desc": "계획적이고 전략적인 INTJ는 자유로운 ENFP, ENTP와 좋은 궁합을 이룹니다.",
        "image": "https://images.unsplash.com/photo-1501706362039-c6e08e1e1f06"  # 늑대
    },
    "ENFJ": {
        "match": ["INFP", "ISFP"],
        "desc": "따뜻하고 배려심 많은 ENFJ는 이상적인 INFP, 자유로운 ISFP와 좋은 관계를 형성합니다.",
        "image": "https://images.unsplash.com/photo-1546182990-dffeafbe841d"  # 코끼리
    },
}

# 웹 앱 제목
st.title("💖 MBTI 궁합 추천")
st.write("당신의 MBTI를 선택하면 궁합이 좋은 MBTI와 설명, 그리고 해당 MBTI를 상징하는 동물 이미지를 보여드립니다!")

# MBTI 선택
user_mbti = st.selectbox("당신의 MBTI를 선택하세요:", list(mbti_data.keys()))

if user_mbti:
    st.subheader(f"💌 {user_mbti}와 잘 맞는 MBTI")
    st.image(mbti_data[user_mbti]["image"], width=400)
    st.markdown(f"**설명:** {mbti_data[user_mbti]['desc']}")
    
    st.write("궁합 최고 MBTI:")
    for m in mbti_data[user_mbti]["match"]:
        st.markdown(f"- 💕 **{m}**")
