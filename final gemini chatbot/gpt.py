import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
ai_api = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=ai_api)

st.set_page_config("OPEN AI CHATBOT", page_icon="ai.png")
st.header("🎀 FINAL CHATBOT PROJECT 🛞")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]): 
        st.markdown(message["content"])

prompt = st.chat_input("Ask to GPT...")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    conversation_history = [
        {"role": message["role"], "content": message["content"]}
        for message in st.session_state.chat_history
    ]
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro")
        response = model.generate_content(
            prompt,
            # context=conversation_history
            )
        response_content = response.text
        
        st.session_state.chat_history.append({"role": "assistant", "content": response_content})
        
        with st.chat_message("assistant"):
            st.markdown(response_content)
        print(conversation_history)
    
    except Exception as e:
        st.error(f"Error: {e}")
