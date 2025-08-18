import streamlit as st
import datetime as dt
import math
from dataclasses import dataclass

# =========================
# 기본 테이블
# =========================
STEMS = ["갑(甲)","을(乙)","병(丙)","정(丁)","무(戊)","기(己)","경(庚)","신(辛)","임(壬)","계(癸)"]
BRANCHES = ["자(子)","축(丑)","인(寅)","묘(卯)","진(辰)","사(巳)","오(午)","미(未)","신(申)","유(酉)","술(戌)","해(亥)"]
BRANCH_ANIMALS = ["쥐🐭","소🐮","호랑이🐯","토끼🐰","용🐲","뱀🐍","말🐴","양🐑","원숭이🐵","닭🐔","개🐶","돼지🐷"]

STEM_ELEMENT = {
    "갑(甲)":"목","을(乙)":"목","병(丙)":"화","정(丁)":"화","무(戊)":"토","기(己)":"토","경(庚)":"금","신(辛)":"금","임(壬)":"수","계(癸)":"수"
}
STEM_YINYANG = { # 양: True, 음: False
    "갑(甲)":True,"을(乙)":False,"병(丙)":True,"정(丁)":False,"무(戊)":True,"기(己)":False,"경(庚)":True,"신(辛)":False,"임(壬)":True,"계(癸)":False
}
BRANCH_ELEMENT = {
    "자(子)":"수","축(丑)":"토","인(寅)":"목","묘(卯)":"목","진(辰)":"토","사(巳)":"화",
    "오(午)":"화","미(未)":"토","신(申)":"금","유(酉)":"금","술(戌)":"토","해(亥)":"수"
}

# 월간 시작(寅月) 테이블: 해당 연간 그룹에서 寅月(1월)의 천간
# 甲·己年: 丙, 乙·庚年: 戊, 丙·辛年: 庚, 丁·壬年: 壬, 戊·癸年: 甲
MONTH_START_BY_YEAR_STEM = {
    "갑(甲)":"병(丙)","기(己)":"병(丙)",
    "을(乙)":"무(戊)","경(庚)":"무(戊)",
    "병(丙)":"경(庚)","신(辛)":"경(庚)",
    "정(丁)":"임(壬)","임(壬)":"임(壬)",
    "무(戊)":"갑(甲)","계(癸)":"갑(甲)"
}
# 寅月을 1로 두고 월지(월의 지지)는 寅→卯→... 순환
MONTH_BRANCH_SEQ = ["인(寅)","묘(卯)","진(辰)","사(巳)","오(午)","미(未)","신(申)","유(酉)","술(戌)","해(亥)","자(子)","축(丑)"]

# 도화(桃花) 규칙: 본명(일지 또는 년지)의 삼합그룹에 따른 도화지지
# 申子辰 → 酉, 亥卯未 → 子, 寅午戌 → 卯, 巳酉丑 → 午
PEACH_BLOSSOM_FOR_GROUP = {
    "신(申)자(子)진(辰)":"유(酉)",
    "해(亥)묘(卯)미(未)":"자(子)",
    "인(寅)오(午)술(戌)":"묘(卯)",
    "사(巳)유(酉)축(丑)":"오(午)"
}

@dataclass
class Pillar:
    stem: str
    branch: str

# =========================
# 보조 함수
# =========================
def lichun_year(date: dt.date) -> int:
    """입춘(간이) 기준: 2월 4일 이전이면 전년도로 간주."""
    y = date.year
    if date.month < 2 or (date.month == 2 and date.day < 4):
        return y - 1
    return y

def year_pillar_by_lichun(date: dt.date) -> Pillar:
    # 간지 주기 기준점: 1984년은 갑자(甲子)년 (양력 2/4 이후 기준)로 널리 사용됨
    # 여기서는 입춘 간이 기준으로 연간/연지 계산
    y = lichun_year(date)
    stem = STEMS[(y - 4) % 10]      # 4년이 갑(甲) 기준
    branch = BRANCHES[(y - 4) % 12] # 4년이 자(子) 기준
    return Pillar(stem, branch)

def month_pillar(date: dt.date, year_stem: str) -> Pillar:
    """
    寅月을 1로 보고(대략 2/4~3/5) 월지/월간 계산 (간이).
    실제는 절기 경계(입춘, 경칩, 청명...) 기준이지만 여기서는 월 경계 간이 근사.
    """
    # 寅月 시작 월/일을 간이로 2/4로 둔다.
    # 寅: ~2/4~3/5, 卯: ~3/6~4/4 ... 정도로 간주하고, 간단히 '2월=寅'부터 12달 순환
    # 월 index 계산
    # 2월을 1, 3월=2, ... 1월=12
    m = date.month
    idx = (m - 2) % 12  # 0..11
    m_branch = MONTH_BRANCH_SEQ[idx]

    # 寅月의 월간 시작을 연간 그룹으로부터 결정하고, 이후 달은 순차 +1
    start_stem = MONTH_START_BY_YEAR_STEM[year_stem]
    start_idx = STEMS.index(start_stem)
    m_stem = STEMS[(start_idx + idx) % 10]
    return Pillar(m_stem, m_branch)

def day_pillar_approx(date: dt.date) -> Pillar:
    """
    일주(간지) 근사치: 서기 1984-02-04(입춘) ≈ 甲子(갑자)일 기준으로 단순 오프셋 적용.
    ※ 주의: 천문력 미사용 근사치.
    """
    base = dt.date(1984, 2, 4) # 기준일 (갑자일로 가정)
    days = (date - base).days
    stem = STEMS[(days) % 10]
    branch = BRANCHES[(days) % 12]
    return Pillar(stem, branch)

def hour_pillar_approx(hour_24: int, day_stem: str) -> Pillar:
    """
    시주(간지) 근사치: 자시=23~01을 0번으로, 2시간 단위 인덱스.
    시지: 자, 축, 인, ... 순환 / 시간: 일간에 따라 정해지는 자시의 시작간에서 +index
    """
    # 2시간 단위 인덱스 만들기 (23~01 → 0, 01~03 → 1, ..., 21~23 → 11)
    # 입력이 "모름"이면 None 처리
    # 자시 기준 지지
    hour_to_index = [11,0,1,2,3,4,5,6,7,8,9,10,11,0,1,2,3,4,5,6,7,8,9,10]  # 0..23 → 0..11 매핑(자시=23,0)
    h_idx = hour_to_index[hour_24]
    h_branch = BRANCHES[(0 + h_idx) % 12]  # 자부터

    # 자시의 시간 시작: 일간 그룹에 따라
    # 갑·기: 甲, 乙·경: 丙, 丙·신: 戊, 丁·임: 庚, 戊·계: 壬 (시작간)
    start_by_daystem = {
        "갑(甲)":"갑(甲)","기(己)":"갑(甲)",
        "을(乙)":"병(丙)","경(庚)":"병(丙)",
        "병(丙)":"무(戊)","신(辛)":"무(戊)",
        "정(丁)":"경(庚)","임(壬)":"경(庚)",
        "무(戊)":"임(壬)","계(癸)":"임(壬)"
    }
    s0 = start_by_daystem[day_stem]
    s0_idx = STEMS.index(s0)
    h_stem = STEMS[(s0_idx + h_idx) % 10]
    return Pillar(h_stem, h_branch)

def ten_gods(day_stem: str, other_stem: str) -> str:
    """
    십성 판별: 일간 기준 오행 상생/상극 + 음양 동일/상반
    - 같은 오행: 비견(양양)/겁재(음양 반대)
    - 일간이 생해주는 쪽: 식신(양양)/상관(음양 반대)
    - 일간을 생해주는 쪽: 편인(양양)/정인(음양 반대)
    - 일간이 극하는 쪽: 편재(양양)/정재(음양 반대)
    - 일간에게 극을 당하는 쪽: 칠살(양양)/정관(음양 반대)
    """
    e_day = STEM_ELEMENT[day_stem]
    e_o = STEM_ELEMENT[other_stem]
    y_day = STEM_YINYANG[day_stem]
    y_o = STEM_YINYANG[other_stem]

    # 상생/상극 관계
    order = ["목","화","토","금","수"]  # 목생화, 화생토, 토생금, 금생수, 수생목
    idx_d = order.index(e_day)
    if e_o == e_day:
        return "비견" if y_day == y_o else "겁재"
    elif e_o == order[(idx_d+1)%5]:  # 내가 생해줌
        return "식신" if y_day == y_o else "상관"
    elif e_o == order[(idx_d-1)%5]:  # 나를 생해줌
        return "편인" if y_day == y_o else "정인"
    elif e_o == order[(idx_d+2)%5]:  # 내가 극함
        return "편재" if y_day == y_o else "정재"
    else:  # 나를 극함 (order[(idx_d-2)%5])
        return "칠살" if y_day == y_o else "정관"

def element_score(pillars: list[Pillar]) -> dict:
    """오행 점수(간+지지 단순 합산, 토는 약간 가중)"""
    score = {"목":0,"화":0,"토":0,"금":0,"수":0}
    for p in pillars:
        score[STEM_ELEMENT[p.stem]] += 1
        score[BRANCH_ELEMENT[p.branch]] += 0.8  # 지지는 가중치 다르게
    return score

def score_comment(score: dict) -> str:
    # 가장 강/약한 오행에 대한 간단 코멘트
    strongest = max(score, key=score.get)
    weakest = min(score, key=score.get)
    tips = {
        "목":"계획·성장·배움에 강점. 관성/규범(금) 보완을 의식해요.",
        "화":"열정·표현·리더십 발휘. 안정감(수·토)으로 균형 잡기.",
        "토":"안정·책임·신뢰 강점. 유연함(목)과 추진력(화) 보강.",
        "금":"분석·결단·정리 강점. 감성(수)과 확장(목)으로 완화.",
        "수":"직관·소통·적응 강점. 실행력(화)과 구조(토) 보강."
    }
    return f"가장 강한 오행: **{strongest}**, 가장 약한 오행: **{weakest}**.\n- 균형 팁: {tips[strongest]}"

def peach_blossom_branch(main_branch: str) -> str | None:
    for group, pb in PEACH_BLOSSOM_FOR_GROUP.items():
        if main_branch in group:
            return pb
    return None

def next_years_with_branch(start_year: int, target_branch: str, count: int=2):
    years = []
    y = start_year
    while len(years) < count and y < start_year + 30:
        if BRANCHES[(y - 4) % 12] == target_branch:
            years.append(y)
        y += 1
    return years

# =========================
# Streamlit UI
# =========================
st.set_page_config(page_title="정통에 가까운 사주풀이", page_icon="🔮", layout="centered")

st.markdown("""
<style>
  .main { background:#FFF5F7; }
  .title { font-size:2.2em; color:#FF6F91; text-align:center; font-weight:800; }
  .card { background:#fff; padding:20px; border-radius:20px; box-shadow:2px 4px 14px rgba(0,0,0,0.08); margin-top:18px; }
  .subtitle { font-size:1.2em; color:#6A0572; font-weight:700; margin-bottom:10px; }
  .kv { font-size:1.05em; margin:6px 0; }
  .muted { color:#777; font-size:0.92em; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🔮 정통에 가까운 사주 & 운세 보기</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("이름")
with col2:
    know_time = st.radio("태어난 시간", ["모름","알아요"], horizontal=True)

birthdate = st.date_input("생년월일", value=dt.date(2000,1,1))

birth_hour = None
if know_time == "알아요":
    # 한국식 12지시 선택도 제공
    mode = st.radio("입력 방식", ["시(0~23시)","지시(자·축·...·해)"], horizontal=True)
    if mode == "시(0~23시)":
        birth_hour = st.slider("태어난 시각(0~23)", 0, 23, 12)
    else:
        zi_list = ["자(23~01)","축(01~03)","인(03~05)","묘(05~07)","진(07~09)","사(09~11)","오(11~13)","미(13~15)","신(15~17)","유(17~19)","술(19~21)","해(21~23)"]
        pick = st.selectbox("태어난 지시", zi_list, index=6)
        # 중앙값 시각으로 환산
        centers = [0,2,4,6,8,10,12,14,16,18,20,22]  # 자~해 블록의 중앙 시각
        birth_hour = centers[zi_list.index(pick)]

st.markdown('<div class="muted">※ 본 앱은 입춘(2/4) 기준·절기 간이 모델과 일/시주 근사치 알고리즘을 사용합니다. 실제 전문 사주풀이와 일부 차이가 있을 수 있어요.</div>', unsafe_allow_html=True)

if st.button("✨ 사주풀이 보기"):
    if not name.strip():
        st.warning("이름을 입력해 주세요!")
    else:
        # 1) 연주(입춘 기준)
        Y = year_pillar_by_lichun(birthdate)

        # 2) 월주(寅月 시작, 간이)
        M = month_pillar(birthdate, Y.stem)

        # 3) 일주(근사)
        D = day_pillar_approx(birthdate)

        # 4) 시주(선택·근사)
        H = None
        if birth_hour is not None:
            H = hour_pillar_approx(birth_hour, D.stem)

        # 표시 카드: 4주
        st.markdown('<div class="card"><div class="subtitle">📜 사주팔자(四柱)</div>', unsafe_allow_html=True)
        def gz(p: Pillar):
            return f"{p.stem} {p.branch}"
        st.markdown(f"<div class='kv'><b>년주:</b> {gz(Y)}  ({BRANCH_ANIMALS[BRANCHES.index(Y.branch)]})</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kv'><b>월주:</b> {gz(M)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kv'><b>일주:</b> {gz(D)}  <span class='muted'>(근사)</span></div>", unsafe_allow_html=True)
        if H:
            st.markdown(f"<div class='kv'><b>시주:</b> {gz(H)}  <span class='muted'>(근사)</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='kv'><b>시주:</b> 시간 미입력</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 십성: 일간 기준, 연/월/시의 천간 해석
        tg_rows = []
        tg_rows.append(("년간", Y.stem, ten_gods(D.stem, Y.stem)))
        tg_rows.append(("월간", M.stem, ten_gods(D.stem, M.stem)))
        if H:
            tg_rows.append(("시간", H.stem, ten_gods(D.stem, H.stem)))

        # 오행 밸런스
        pillars_for_score = [Y, M, D] + ([H] if H else [])
        score = element_score(pillars_for_score)

        st.markdown('<div class="card"><div class="subtitle">🌈 오행 밸런스 & 십성(十神)</div>', unsafe_allow_html=True)
        s_line = " · ".join([f"{k}:{round(v,1)}" for k,v in score.items()])
        st.markdown(f"<div class='kv'><b>오행 점수(간+지지):</b> {s_line}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kv'>{score_comment(score)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='kv'><b>십성 해석(일간 기준 다른 천간):</b></div>", unsafe_allow_html=True)
        for label, stem, tg in tg_rows:
            st.markdown(f"<div class='kv'>- {label}: {stem} → <b>{tg}</b></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 간단 성향/조언
        stem_traits = {
            "목":"성장·배움·유연성, 관계에서 진정성 중시",
            "화":"표현·리더십·열정, 진취적·낙관적",
            "토":"안정·책임·신뢰, 신중하고 현실적",
            "금":"분석·규범·정리, 기준과 품질 중시",
            "수":"직관·소통·적응, 감수성과 통찰"
        }
        st.markdown('<div class="card"><div class="subtitle">🧭 기본 성향 요약</div>', unsafe_allow_html=True)
        st.markdown(f"<div class='kv'>일간(나의 기운): <b>{D.stem}</b> → {stem_traits[STEM_ELEMENT[D.stem]]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kv'>연지(기본 기질): <b>{Y.branch}</b>({BRANCH_ANIMALS[BRANCHES.index(Y.branch)]})</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 연애/직업/재물/건강 + 연애 시기(도화 활용)
        # 도화 기준: 일지 우선, 없으면 년지 사용
        main_branch = D.branch if D else Y.branch
        pb = peach_blossom_branch(main_branch)
        this_year = dt.date.today().year
        love_when = "연애 타이밍: 데이터를 충분히 산정할 수 없어요."
        if pb:
            nyrs = next_years_with_branch(this_year, pb, 2)
            if nyrs:
                if len(nyrs) == 1:
                    love_when = f"💘 도화(桃花) 기운이 강한 해: <b>{nyrs[0]}년</b>"
                else:
                    love_when = f"💘 도화(桃花) 강세 해: <b>{nyrs[0]}년</b>, <b>{nyrs[1]}년</b>"
        # 간단 운세 문구(오행 밸런스 기반)
        strongest = max(score, key=score.get)
        weakest = min(score, key=score.get)
        love_msg = {
            "목":"관계에 성장과 배려가 흐릅니다. 속도 조절로 안정감을!",
            "화":"끌림과 표현력이 커집니다. 말보다 행동의 일관성을!",
            "토":"신뢰가 매력 포인트. 과한 신중함은 타이밍을 놓칠 수 있어요.",
            "금":"기준이 높아 선별적 매칭. 유연함을 더하면 인연이 빨라져요.",
            "수":"소통과 공감력이 강점. 감정 기복만 관리하면 순항!"
        }[strongest]
        job_msg = {
            "목":"기획·교육·콘텐츠에 길. 새 프로젝트에 도전!",
            "화":"영업·리더십·대외활동 호조. 존재감 업!",
            "토":"관리·운영·재무 안정. 지속성으로 승부!",
            "금":"품질·분석·법무·기준 수립에 강점.",
            "수":"연구·데이터·소통 직무 유리. 네트워킹 확장!"
        }[strongest]
        money_msg = {
            "목":"투자는 분산과 장기로. 배움에 쓰는 돈이 수익으로 돌아와요.",
            "화":"수입 변동성 관리가 핵심. 지출 예산을 고정하세요.",
            "토":"안정 자산 선호가 이점. 꾸준한 적립이 답.",
            "금":"리밸런싱·리스크관리로 수익률 개선.",
            "수":"정보 비대칭을 기회로. 타이밍 포착!"
        }[strongest]
        health_msg = {
            "목":"근지구력·유연성 운동이 이점.",
            "화":"심폐 강화, 수분 보충을 의식!",
            "토":"자세 교정·코어 강화로 체력 기초 다지기.",
            "금":"과로·근골격 관리. 규칙적 스트레칭!",
            "수":"수면 리듬·마음 돌봄이 핵심."
        }[strongest]

        st.markdown('<div class="card"><div class="subtitle">✨ 오늘의 해석 & 운세</div>', unsafe_allow_html=True)
        st.markdown(f"<div class='kv'><b>연애운:</b> {love_msg}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kv'><b>직업운:</b> {job_msg}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kv'><b>재물운:</b> {money_msg}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kv'><b>건강운:</b> {health_msg}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kv'><b>연애 시기 예측(도화 기반):</b> {love_when}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 마지막 안내
        st.markdown("""
<div class="card">
  <div class="subtitle">ℹ️ 참고 안내</div>
  <div class="kv muted">
    - 본 앱은 절기 간이 경계(입춘 2/4)와 일/시주 근사 알고리즘을 이용합니다.<br/>
    - 전문 명리에서는 천문력(24절기 정확 경계, 대운·세운 등)을 함께 고려합니다.<br/>
    - 필요하면 “정확 절기/대운 계산 API” 연동 구조로 확장할 수 있어요.
  </div>
</div>
""", unsafe_allow_html=True)
