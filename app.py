import streamlit as st
from openai import OpenAI
import json
import os

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="Anurag University Career Assistant",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------------------------------
# API KEY
# -------------------------------------------------------

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OPENAI_API_KEY not found.")
    st.info(
        "Add your API key in:\n\n"
        "Streamlit Cloud → Settings → Secrets\n\n"
        "or\n\n"
        ".streamlit/secrets.toml"
    )
    st.stop()

client = OpenAI(api_key=api_key)

# -------------------------------------------------------
# CHAT HISTORY FILE
# -------------------------------------------------------

CHAT_FILE = "chat_history.json"

SYSTEM_PROMPT = {
    "role": "system",
    "content": """
You are Anurag University Placement & Career Assistant.

Help students with:

• Placements
• IT Jobs
• Government Jobs
• Resume Building
• Interview Preparation
• Aptitude
• Coding
• Communication Skills
• Career Guidance
• Higher Studies
• Internships

Always answer in simple English.
If suitable, you may also use Tenglish.
Give practical and realistic advice.
"""
}


# -------------------------------------------------------
# LOAD CHAT
# -------------------------------------------------------

def load_chat():

    if os.path.exists(CHAT_FILE):

        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    return [SYSTEM_PROMPT]


# -------------------------------------------------------
# SAVE CHAT
# -------------------------------------------------------

def save_chat(messages):

    with open(CHAT_FILE, "w", encoding="utf-8") as f:

        json.dump(
            messages,
            f,
            indent=4,
            ensure_ascii=False
        )


# -------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = load_chat()


# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

with st.sidebar:

    st.title("🎓 Anurag University Career Assistant")

    st.divider()

    st.subheader("📜 Previous Searches")

    questions = [
        msg["content"]
        for msg in st.session_state.messages
        if msg["role"] == "user"
    ]

    if len(questions) == 0:

        st.write("No searches yet.")

    else:

        for i, q in enumerate(reversed(questions), start=1):

            st.markdown(f"**{i}.** {q}")

    st.divider()

    if st.button("🗑 Clear Chat History", use_container_width=True):

        st.session_state.messages = [SYSTEM_PROMPT]

        save_chat(st.session_state.messages)

        st.success("History Cleared!")

        st.rerun()


# -------------------------------------------------------
# MAIN PAGE
# -------------------------------------------------------

st.title("🎓 Anurag University Placement & Career Assistant")

st.write(
    "Ask anything about placements, internships, resume, coding, interviews, government jobs, or career guidance."
)

# -------------------------------------------------------
# DISPLAY CHAT
# -------------------------------------------------------

for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -------------------------------------------------------
# USER INPUT
# -------------------------------------------------------

prompt = st.chat_input("Type your question here...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    save_chat(st.session_state.messages)

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        placeholder.markdown("⏳ Thinking...")

        try:

            response = client.chat.completions.create(

                model="gpt-4.1-mini",

                messages=st.session_state.messages,

                temperature=0.7
            )

            answer = response.choices[0].message.content

            placeholder.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            save_chat(st.session_state.messages)

        except Exception as e:

            placeholder.error(f"Error: {e}")
