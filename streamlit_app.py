import streamlit as st
import openai
import os

# 페이지 설정 및 스타일 적용
st.set_page_config(page_title="마음솔", page_icon="💖")

# CSS 스타일 추가
st.markdown("""
<style>
    /* 제목 및 소개글 스타일링 */
    .title {
        text-align: center;
        color: #FF69B4;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        text-shadow: 0px 1px 2px rgba(0,0,0,0.1);
    }
    .intro {
        text-align: center;
        color: #555;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        line-height: 1.6;
    }
    /* 컨테이너 스타일링 */
    .container {
        background-color: #FFF5F7;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
    }
    /* 채팅 영역 스타일링 */
    .chat-container {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 헤더 섹션 - 가운데 정렬된 제목과 소개글
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<h1 class="title">💖 마음솔 💖</h1>', unsafe_allow_html=True)
st.markdown('<p class="intro">혼자 고민하기 어려운 순간, 가볍게 이야기 나눌 수 있는 마음 토크 친구예요. 💛</p>', unsafe_allow_html=True)
st.markdown('<p class="intro">어떤 이야기도 괜찮아요. 편안한 마음으로 찾아와 주세요. 😊</p>', unsafe_allow_html=True)
st.markdown('<p class="intro">함께 생각해보고, 조금 더 가벼운 마음이 될 수 있도록 도와드릴게요!</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# API 키 입력란
openai_api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))

if not openai_api_key:
    openai_api_key = st.text_input("🔑 OpenAI API Key를 입력해 주세요 😊", type="password")
    if openai_api_key:
        st.success("✅ API 키가 입력되었습니다! 대화를 시작할 수 있어요.")

if not openai_api_key:
    st.warning("🔒 OpenAI API Key를 입력해야 대화를 시작할 수 있어요!", icon="🗝️")
    st.stop()

# OpenAI 클라이언트 생성
try:
    client = openai.OpenAI(api_key=openai_api_key)
except Exception as e:
    st.error(f"🚨 OpenAI API 클라이언트를 생성하는 중 오류 발생: {e}")
    st.stop()

# 초기 메시지 설정 - API 키 입력 후 바로 인사 메시지 표시
if "messages" not in st.session_state:
    st.session_state.messages = []

# API 키 입력 후 초기 메시지 추가
if openai_api_key and not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": "안녕하세요, 오늘은 어떤 대화를 하고 싶으신가요? 😊"})

# 채팅 컨테이너 시작
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# 기존 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("무엇이든 편하게 이야기해 주세요."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAI API 호출 (예외 처리 추가)
    try:
        with st.spinner("생각 중..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )

        # 응답 데이터 확인 및 저장
        if response and response.choices:
            assistant_response = response.choices[0].message.content
            with st.chat_message("assistant"):
                st.markdown(assistant_response)

            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        else:
            st.error("⚠️ 응답이 비어 있습니다. 다시 시도해 주세요.")

    except Exception as e:
        if "401" in str(e):
            st.error("🚨 OpenAI API 호출 중 오류 발생: 잘못된 API 키입니다. API 키를 다시 확인해 주세요.")
        else:
            st.error(f"🚨 OpenAI API 호출 중 오류 발생: {e}")

# 채팅 컨테이너 종료
st.markdown('</div>', unsafe_allow_html=True)
