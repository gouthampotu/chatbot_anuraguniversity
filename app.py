import streamlit as st
from openai import OpenAI

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Anurag University Placement & Career Assistant",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------------------------
# OPENAI API
# -------------------------------------------------
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.error("❌ OPENAI_API_KEY not found.")
    st.info("Add your API key in Streamlit Secrets.")
    st.stop()

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.title("🎓 Anurag University Placement & Career Assistant")
st.write(
    "Ask questions about placements, internships, resumes, coding, interviews, government jobs, and career guidance."
)

# -------------------------------------------------
# SYSTEM PROMPT
# -------------------------------------------------
SYSTEM_PROMPT = {
    "role": "system",
    "content": """
You are a career assistant for Bhilwara students.

Help students with:
- Placements
- IT Jobs
- Government Jobs
- Resume Building
- Interview Preparation
- Coding
- Communication Skills
- Internships
- Higher Studies

Use simple English.
If needed, use Tenglish.
Give practical advice.
"""
}

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [SYSTEM_PROMPT]

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
with st.sidebar:

    st.header("📜 Previous Questions")

    questions = [
        msg["content"]
        for msg in st.session_state.messages
        if msg["role"] == "user"
    ]

    if len(questions) == 0:
        st.info("No previous questions.")

    else:
        for i, q in enumerate(reversed(questions), start=1):
            st.write(f"**{i}.** {q}")

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = [SYSTEM_PROMPT]
        st.rerun()

# -------------------------------------------------
# DISPLAY CHAT
# -------------------------------------------------
for msg in st.session_state.messages:

    if msg["role"] == "system":
        continue

    avatar = "👨‍🎓" if msg["role"] == "user" else "🤖"

    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# -------------------------------------------------
# CHAT INPUT
# -------------------------------------------------
prompt = st.chat_input("Ask your question...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user", avatar="👨‍🎓"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):

        placeholder = st.empty()

        with st.spinner("Thinking..."):

            try:

                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=st.session_state.messages,
                    temperature=0.7,
                )

                answer = response.choices[0].message.content

                placeholder.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:
                placeholder.error(f"Error: {e}")
