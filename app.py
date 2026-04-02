import streamlit as st
import asyncio
import nest_asyncio
from main import main

nest_asyncio.apply()

st.set_page_config(page_title="MCP Chat", page_icon="📊", layout="centered")
st.title("📊 MCP Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask about your expenses...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.get_event_loop().run_until_complete(main(prompt))
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
