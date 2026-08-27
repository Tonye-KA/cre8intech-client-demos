import streamlit as st
import openai
import urllib.parse

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

    /* Primary Buttons */
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
        margin-top: 8px;
    }
    .wa-btn:hover {
        background-color: #1EBE5D;
        color: #FFFFFF !important;
    }

    /* Demo Badge & Cards */
    .demo-badge {
        background-color: #10B981;
        color: white !important;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    
    .dispatch-box {
        background-color: #FFFFFF;
        border: 1px solid #10B981;
        border-radius: 10px;
        padding: 14px;
        margin-top: 15px;
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
1. MODULE 1 (Socratic Step-by-Step Problem Solver): NEVER dump the final answer immediately. Break problems into 3-4 structured, easy-to-digest steps.
2. MODULE 2 (Interactive Concept Checker): Always conclude your explanation with a quick 'Concept Check' mini-question to test active student understanding before they move on.
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

# ==========================================
# MODULE 3: REVISION DISPATCH & PARENT SHARE
# ==========================================
user_assistant_msgs = [m for m in st.session_state.messages if m["role"] in ["user", "assistant"]]

if len(user_assistant_msgs) >= 2:
    st.markdown("---")
    st.subheader("📤 Module 3: Revision Dispatch & Parent Summary")
    st.write("Save or share this lesson summary for homework review or parent updates:")
    
    last_user_q = [m["content"] for m in st.session_state.messages if m["role"] == "user"][-1]
    last_bot_a = [m["content"] for m in st.session_state.messages if m["role"] == "assistant"][-1]

    summary_text = (
        f"📚 *Green Obsidian Maths Revision Summary*\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎯 *Question/Topic:* {last_user_q}\n\n"
        f"💡 *Step-by-Step Solution & Notes:*\n{last_bot_a}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"✨ *Green Obsidian Educational Services* | 24/7 Maths Copilot"
    )

    encoded_wa_text = urllib.parse.quote(summary_text)
    wa_share_url = f"https://api.whatsapp.com/send?text={encoded_wa_text}"

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f'<a href="{wa_share_url}" target="_blank" class="wa-btn">📲 Share to WhatsApp (Parent/Student)</a>', unsafe_allow_html=True)
    with col_b:
        st.download_button(
            label="📄 Download Revision Sheet (.txt)",
            data=summary_text,
            file_name="Green_Obsidian_Maths_Revision.txt",
            mime="text/plain",
            use_container_width=True
        )
