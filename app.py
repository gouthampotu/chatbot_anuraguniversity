import streamlit as st
from openai import OpenAI
import json
import os

# ----------------------------
# OpenAI API Key
# ----------------------------
api_key = st.secrets.get("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")

if not api_key:
    st.error("❌ OPENAI_API_KEY not found.")
    st.stop()

client = OpenAI(api_key=api_key)

# ----------------------------
# Streamlit Config
# ----------------------------
st.set_page_config(
    page_title="Anurag University Career Assistant",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Anurag University Placement & Career Assistant")
st.write("Your personalised career assistant.")

# ----------------------------
# Chat History File
# ----------------------------
CHAT_FILE = "chat_history.json"

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
                "You are a placement and career assistant for students in Anurag University. "
                "Guide them for IT jobs, government jobs, internships, resume building, "
                "communication skills, coding basics, interview preparation, "
                "and practical career paths suitable for students from small towns, degree colleges, "
                "and rural backgrounds. Use simple English and optional Tenglish. "
                "Give realistic, actionable advice for Bhilwara students."
    )
}


# ----------------------------
# Load Chat History
# ----------------------------
def load_chat():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    else:
        return [SYSTEM_PROMPT]


# ----------------------------
# Save Chat History
# ----------------------------
def save_chat(messages):
    with open(CHAT_FILE, "w") as f:
        json.dump(messages, f, indent=4)


# ----------------------------
# Session State
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = load_chat()


# ----------------------------
# Sidebar History
# ----------------------------
st.sidebar.title("📜 Previous Searches")

questions = [
    msg["content"]
    for msg in st.session_state.messages
    if msg["role"] == "user"
]

if len(questions) == 0:
    st.sidebar.info("No previous searches.")
else:
    for i, q in enumerate(questions[::-1], 1):
        st.sidebar.write(f"**{i}.** {q}")


# ----------------------------
# Clear Chat Button
# ----------------------------
if st.sidebar.button("🗑 Clear History"):
    st.session_state.messages = [SYSTEM_PROMPT]
    save_chat(st.session_state.messages)
    st.rerun()


# ----------------------------
# Display Chat
# ----------------------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])


# ----------------------------
# User Input
# ----------------------------
prompt = st.chat_input("Ask about careers, placements, resumes...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    save_chat(st.session_state.messages)

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()
        placeholder.write("Thinking...")

        try:

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=st.session_state.messages
            )

            reply = response.choices[0].message.content

            placeholder.write(reply)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

            save_chat(st.session_state.messages)

        except Exception as e:
            placeholder.error(str(e))
