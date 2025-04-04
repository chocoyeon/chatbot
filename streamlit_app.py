import streamlit as st
from openai import OpenAI
import os

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))

# Show title and description.
st.title("💬 yeon's ChatBot")
st.write(
    "혼자 고민하기 어려운 순간, 가볍게 이야기 나눌 수 있는 마음 토크 친구예요. 💛\n"
    "어떤 이야기도 괜찮아요. 편안한 마음으로 찾아와 주세요. 😊\n"
    "함께 생각해 보고, 조금 더 가벼운 마음이 될 수 있도록 도와드릴게요!"
)

if not st.session_state.openai_api_key:
    st.session_state.openai_api_key = st.text_input("🔑 아래 OpenAI API Key를 입력해 주세요 😊", type="password")
#openai_api_key = st.text_input("🔑 OpenAI API Key를 입력해 주세요 😊", type="password")

if not st.session_state.openai_api_key:
    st.warning("🔒 OpenAI API Key를 입력해야 대화를 시작할 수 있어요!", icon="🗝️")
    st.stop()

if "client" not in st.session_state:
    try:
        st.session_state.client = openai.OpenAI(api_key=st.session_state.openai_api_key)
    except Exception as e:
        st.error(f"🚨 OpenAI API 클라이언트를 생성하는 중 오류 발생: {e}")
        st.stop()






if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요, 오늘은 어떤 대화를 하고 싶으신가요? 😊"}
        ]

for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("무엇이든 편하게 이야기해 주세요 ^^"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    )

    with st.chat_message("assistant"):
        assistant_response = response.choices[0].message.content
        st.markdown(assistant_response)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
