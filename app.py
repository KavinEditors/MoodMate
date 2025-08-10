import streamlit as st
import requests
import os
import numpy as np
import pandas as pd

api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY")


st.set_page_config(page_title="MoodMate", page_icon="😶", layout="wide")
st.markdown("<h1 style='text-align:center;'>😶 MoodMate</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Because even your emotions deserve a good friend 💙</p>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "username" not in st.session_state:
    st.session_state.username = ""
if "mood" not in st.session_state:
    st.session_state.mood = "Happy"
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def show_mood_chart():
    st.markdown("### 🧠 Human's Mood")
    mood_labels = ["Happy 😀", "Sad 😢", "Annoyed 😤", "Confused 🤔"]
    raw = np.random.rand(4)
    percentages = (raw / raw.sum() * 100).round().astype(int)
    mood_df = pd.DataFrame({
        "Mood": mood_labels,
        "Percentage": percentages
    })
    st.bar_chart(mood_df.set_index("Mood"), use_container_width=True)

left, center, right = st.columns([2, 5, 2])

with right:
    if st.button("🌃 Dark Mode"):
        st.session_state.theme = "dark"
    if st.button("🌇 Light Mode"):
        st.session_state.theme = "light"

with left:
    st.markdown("### 📝 Name")
    name = st.text_input("Enter your name", value=st.session_state.username)
    if name.strip():
        st.session_state.username = name.strip()
    else:
        st.session_state.username = "User"
    st.markdown("---")
    show_mood_chart()

def moodmate_message(user_msg):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    persona = f"""
    You are MoodMate, a warm, friendly emotional companion.
    The user's name is {st.session_state.username}.
    Step 1: Detect the emotion from their message (happy, sad, annoyed, confused).
    Step 2: Reply naturally like a close friend — relaxed, empathetic, and human.
    Step 3: Keep the reply short: minimum 2 lines, maximum 4 lines.
      - If happy: Share excitement and joy with them.
      - If sad: Offer warmth, hope, and gentle encouragement.
      - If annoyed: Calm them and lighten the mood.
      - If confused: Explain simply and give clear guidance.
    No long speeches, just short and heartfelt responses. also use emogi.
    """
    messages = [{"role": "system", "content": persona}]
    for chat in st.session_state.chat_history:
        messages.append({"role": "user", "content": chat["user"]})
        messages.append({"role": "assistant", "content": chat["bot"]})
    messages.append({"role": "user", "content": user_msg})

    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json={"model": "llama3-8b-8192", "messages": messages}
        )
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def message_align(msg, sender="user"):
    align = "flex-end" if sender == "user" else "flex-start"
    emoji = "😶" if sender == "user" else "😎"
    if st.session_state.theme == "dark":
        border_color = "white"
        text_color = "white"
    else:
        border_color = "black"
        text_color = "black"

    st.markdown(f"""
        <div style='display: flex; justify-content: {align}; margin: 10px 0;'>
            <div style='border: 1.5px solid {border_color}; background-color: transparent;
                        padding: 10px 15px; border-radius: 15px; max-width: 75%;
                        font-size: 16px; color: {text_color};'>
                <span><b>{emoji}</b> {msg}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with center:
    for chat in st.session_state.chat_history:
        message_align(chat["user"], "user")
        message_align(chat["bot"], "bot")

    col1, col2 = st.columns([8, 1])
    with col1:
        user_input = st.text_input(" ", placeholder="Type your message...", label_visibility="collapsed", key="input")
    with col2:
        send = st.button("Send")

    if user_input and send:
        with st.spinner("💬 Understanding your feelings..."):
            response = moodmate_message(user_input)
        st.session_state.chat_history.append({"user": user_input, "bot": response})
        st.rerun()
with center:
    for chat in st.session_state.chat_history:
        message_align(chat["user"], "user")
        message_align(chat["bot"], "bot")

    col1, col2 = st.columns([8, 1])
    with col1:
        user_input = st.text_input(" ", placeholder="Type your message...", label_visibility="collapsed", key="input")
    with col2:
        send = st.button("Send")

    if user_input and send:
        with st.spinner("💬 Understanding your feelings..."):
            response = moodmate_message(user_input)
        st.session_state.chat_history.append({"user": user_input, "bot": response})
        st.rerun()
