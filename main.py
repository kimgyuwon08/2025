import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천", page_icon="💼")

st.title("💼 MBTI 기반 진로 추천 사이트")
st.write("MBTI를 선택하면 적합한 직업을 추천해드립니다!")

# MBTI 목록
mbti_types = ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", 
              "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]

mbti = st.selectbox("당신의 MBTI를 선택하세요:", mbti_types)

# 직업 데이터
mbti_jobs = {
    "INTJ": {
        "직업": ["전략기획가", "데이터 분석가", "연구원", "엔지니어"],
        "설명": "독창적이고 전략적인 성향을 가진 INTJ는 장기적인 계획과 분석이 필요한 분야에서 강점을 발휘합니다."
    },
    "ENFP": {
        "직업": ["광고 기획자", "이벤트 플래너", "콘텐츠 크리에이터", "교사"],
        "설명": "창의적이고 사람을 좋아하는 ENFP는 새로운 아이디어를 실현하고 소통하는 직업에 잘 맞습니다."
    },
    # 나머지 MBTI 데이터...
}

if mbti in mbti_jobs:
    st.subheader(f"{mbti} 유형의 추천 직업")
    st.write(mbti_jobs[mbti]["설명"])
    for job in mbti_jobs[mbti]["직업"]:
        st.markdown(f"- {job}")
else:
    st.warning("아직 해당 MBTI의 데이터가 없습니다.")

