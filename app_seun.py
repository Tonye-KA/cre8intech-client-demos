import streamlit as st
import openai

# Page Setup
st.set_page_config(page_title="MathsBot | Green Obsidian", page_icon="📐", layout="centered")

# Custom Brand Styling (Green Obsidian Palette)
st.markdown("""
    <style>
    .stApp {
        background-color: #F0FDF4;
    }
    h1 {
        color: #0F382C !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stButton>button {
        background-color: #0F382C;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 16px;
    }
    .stButton>button:hover {
        background-color: #10B981;
        color: white;
    }
    .demo-badge {
        background-color: #10B981;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<span class="demo-badge">CRE8INTECH PROTOTYPE DEMO</span>', unsafe_allow_html=True)
st.title("📐 MathsBot — Year 6 Exam Companion")
st.caption("Configured for **Green Obsidian Educational Services**")

SYSTEM_PROMPT = """
You are 'MathsBot', an encouraging Year 6 Primary School Maths Tutor for Green Obsidian Educational Services.
Target audience: 10-11 year old students preparing for secondary entrance exams.

RULES:
1. NEVER give the raw answer immediately. Guide step-by-step in 3-4 clear points.
2. Use simple, supportive language with primary-friendly formatting.
3. End with a short check question (e.g., "Ready to try a similar problem?").
"""

api_key = st.secrets.get("OPENAI_API_KEY", "")
client = openai.OpenAI(api_key=api_key) if api_key else None

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

st.markdown("**Quick Sample Questions:**")
col1, col2 = st.columns(2)
with col1:
    if st.button("How do I add 2/3 + 1/4?"):
        st.session_state.user_prompt = "How do I add 2/3 + 1/4?"
with col2:
    if st.button("Explain ratios in simple steps"):
        st.session_state.user_prompt = "Explain ratios in simple steps for entrance exams"

user_input = st.chat_input("Ask MathsBot a question...") or st.session_state.pop("user_prompt", None)

if user_input:
    if not client:
        st.error("Please add your API Key in Streamlit Secrets.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )
        bot_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.write(bot_reply)
