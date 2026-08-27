import streamlit as st
import openai
import urllib.parse
from datetime import datetime

# Page Setup
st.set_page_config(page_title="MathsBot | Green Obsidian", page_icon="📐", layout="centered")

# Custom Brand Styling (Green Obsidian Palette)
st.markdown("""
    <style>
    /* Main Background & Text */
    .stApp {
        background-color: #F0FDF4 !important;
        color: #0F382C !important;
    }
    
    h1, h2, h3, p, span, label {
        color: #0F382C !important;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Chat Message Content */
    [data-testid="stChatMessageContent"] {
        background-color: #FFFFFF !important;
        color: #0F382C !important;
        border-radius: 10px;
        padding: 12px;
        border: 1px solid #10B981;
    }
    
    [data-testid="stChatMessageContent"] p, 
    [data-testid="stChatMessageContent"] li, 
    [data-testid="stChatMessageContent"] div {
        color: #0F382C !important;
        font-weight: 500;
    }

    /* Primary Action Buttons */
    div.stButton > button {
        background-color: #0F382C !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 16px !important;
        width: 100%;
    }

    div.stButton > button * {
        color: #FFFFFF !important;
        font-weight: bold !important;
    }

    div.stButton > button:hover {
        background-color: #10B981 !important;
    }

    /* WhatsApp Action Button */
    .wa-btn {
        display: block;
        text-align: center;
        background-color: #25D366;
        color: #FFFFFF !important;
        font-weight: bold;
        padding: 10px 16px;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 2px;
    }
    .wa-btn:hover {
        background-color: #1EBE5D;
        color: #FFFFFF !important;
    }

    /* Demo Badge */
    .demo-badge {
        background-color: #10B981;
        color: white !important;
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

CORE PEDAGOGICAL RULES:
1. MODULE 1 (Socratic Step-by-Step Problem Solver): NEVER dump the final raw answer immediately. Break problems down into 3-4 structured, easy-to-digest steps.
2. MODULE 2 (Interactive Concept Checker): Conclude your explanation with a quick 'Concept Check' mini-question to test active student understanding.
3. Keep the tone warm, highly encouraging, and clear for exam revision.
"""

api_key = st.secrets.get("OPENAI_API_KEY", "")
client = openai.OpenAI(api_key=api_key) if api_key else None

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Render Conversation History
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Quick Question Triggers
st.markdown("**Quick Sample Questions:**")
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ How do I add 2/3 + 1/4?"):
        st.session_state.user_prompt = "How do I add 2/3 + 1/4? Please walk me through step-by-step."
with col2:
    if st.button("📊 Explain ratios in simple steps"):
        st.session_state.user_prompt = "Explain ratios in simple steps for secondary school entrance exams."

user_input = st.chat_input("Ask MathsBot a maths problem or revision topic...") or st.session_state.pop("user_prompt", None)

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

# ==============================================================
# FULL-SESSION COMPILATION & REVISION NOTES DISPATCH
# ==============================================================
user_assistant_msgs = [m for m in st.session_state.messages if m["role"] in ["user", "assistant"]]

if len(user_assistant_msgs) >= 2:
    st.markdown("---")
    st.subheader("📥 Save Lesson & Revision Notes")
    st.caption("Download or share the complete summary of all questions and worked solutions from this study session:")

    # Compile the entire study session into one cohesive revision sheet
    session_date = datetime.now().strftime("%d %b %Y, %I:%M %p")
    full_session_summary = f"📚 GREEN OBSIDIAN MATHS REVISION SHEET\n"
    full_session_summary += f"📅 Session Date: {session_date}\n"
    full_session_summary += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    q_count = 1
    # Pair each question with its answer
    for i in range(0, len(user_assistant_msgs), 2):
        if i + 1 < len(user_assistant_msgs):
            q_text = user_assistant_msgs[i]["content"]
            a_text = user_assistant_msgs[i+1]["content"]
            full_session_summary += f"🎯 [TOPIC/QUESTION {q_count}]: {q_text}\n\n"
            full_session_summary += f"💡 [WORKED SOLUTION & NOTES]:\n{a_text}\n\n"
            full_session_summary += f"────────────────────────────────────\n\n"
            q_count += 1

    full_session_summary += "✨ Green Obsidian Educational Services | 24/7 Maths Copilot"

    # Encode for WhatsApp Link
    encoded_wa_text = urllib.parse.quote(full_session_summary)
    wa_share_url = f"https://api.whatsapp.com/send?text={encoded_wa_text}"

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f'<a href="{wa_share_url}" target="_blank" class="wa-btn">📲 Share Full Session (WhatsApp)</a>', unsafe_allow_html=True)
    with col_b:
        st.download_button(
            label="📄 Download Full Session Notes (.txt)",
            data=full_session_summary,
            file_name=f"Green_Obsidian_Study_Session_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
