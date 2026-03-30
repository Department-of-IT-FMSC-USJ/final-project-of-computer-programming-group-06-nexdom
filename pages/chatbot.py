import streamlit as st
from chatbot.rag_chatbot import RAGChatBot

# Check login
if "db" not in st.session_state:
    st.warning("⚠️ Please go to Home page first.")
    st.stop()

if not st.session_state.get("logged_in") or st.session_state.user_role != "customer":
    st.warning("⚠️ Login as **Customer** to use ChatBot.")
    st.stop()

db = st.session_state.db

# ==========================================
# AUTO-CONNECT WITH API KEY (NO USER INPUT)
# ==========================================
API_KEY = "AIzaSyB7eqZ0Yf0f9iR1pq4r6t5OwM6knyV_A2U"  # <-- Paste your key here

if "rag_bot" not in st.session_state:
    st.session_state.rag_bot = RAGChatBot(
        api_key=API_KEY, db_manager=db
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

bot = st.session_state.rag_bot

# ==========================================
# MAIN PAGE
# ==========================================
st.title("🤖 HomeHelper AI ChatBot")
st.markdown("*Powered by **RAG Architecture** + **Google Gemini AI***")
st.markdown("---")

# ==========================================
# QUICK SERVICE BUTTONS
# ==========================================
st.subheader("⚡ Quick Recommendations")
services = ["plumbing", "carpentry", "electrical", "painting", "cleaning"]
btn_cols = st.columns(5)

for i, col in enumerate(btn_cols):
    with col:
        if st.button(services[i].title(), use_container_width=True, key=f"q_{services[i]}"):
            user_msg = f"Find me the best {services[i]} provider"
            st.session_state.messages.append({"role": "user", "content": user_msg})
            with st.spinner(f"Analyzing {services[i]}..."):
                response = bot.get_service_recommendation(services[i])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

st.markdown("---")

# ==========================================
# CHAT DISPLAY
# ==========================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# CHAT INPUT
# ==========================================
user_input = st.chat_input("Ask me anything about service providers...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            bot_response = bot.chat(user_input)
        st.markdown(bot_response)

    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Clear button
if st.session_state.messages:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()