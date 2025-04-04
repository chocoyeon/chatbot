import streamlit as st
import openai
import os

# 챗봇 UI - 소개글
st.title("💖 마음솔")
st.write("혼자 고민하기 어려운 순간, 가볍게 이야기 나눌 수 있는 마음 토크 친구예요. 💛<br>"
         "어떤 이야기도 괜찮아요. 편안한 마음으로 찾아와 주세요. 😊<br>"
         "함께 생각해보고, 조금 더 가벼운 마음이 될 수 있도록 도와드릴게요!")

# API 키 입력란 
openai_api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))

if not openai_api_key:
    openai_api_key = st.text_input("🔑 OpenAI API Key를 입력해 주세요 😊", type="password")

if not openai_api_key:
    st.warning("🔒 OpenAI API Key를 입력해야 대화를 시작할 수 있어요!", icon="🗝️")
    st.stop()

# OpenAI 클라이언트 생성
try:
    client = openai.OpenAI(api_key=openai_api_key)
except Exception as e:
    st.error(f"🚨 OpenAI API 클라이언트를 생성하는 중 오류 발생: {e}")
    st.stop()

# 초기 메시지
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요, 오늘은 어떤 대화를 하고 싶으신가요? 😊"}
    ]

# 사용자 입력 받기
prompt = st.chat_input("무엇이든 편하게 이야기해 주세요.")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAI API 응답 생성 (예외 처리 추가)
    try:
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
        # API 키 오류 메시지 추가
        if "401" in str(e):
            st.error("🚨 OpenAI API 호출 중 오류 발생: 잘못된 API 키입니다. API 키를 다시 확인해 주세요.")
        else:
            st.error(f"🚨 OpenAI API 호출 중 오류 발생: {e}")
