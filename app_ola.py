import streamlit as st
import openai
import urllib.parse
from datetime import datetime

# Page Setup
st.set_page_config(
    page_title="Financial Diagnostic | Money Wit Africa", 
    page_icon="📊", 
    layout="centered"
)

# Custom Styling (Black Branded Dropdown + Gold Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');

    /* 1. Page Canvas & Spacing */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .main .block-container {
        padding-top: 3.5rem !important;
        max-width: 720px !important;
    }

    /* 2. Headings & Typography */
    h1, h2, h3, h4 {
        font-family: 'Playfair Display', serif !important;
        color: #0F172A !important;
        font-weight: 700 !important;
        line-height: 1.25 !important;
    }

    p, span, label, [data-testid="stMarkdownContainer"] p, [data-testid="stCaptionContainer"] p {
        color: #1E293B !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Question Labels */
    label[data-testid="stWidgetLabel"] p {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 14.5px !important;
    }

    /* 3. Cre8intech Demo Badge */
    .demo-badge {
        background-color: #0F172A !important;
        color: #F59E0B !important;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.2px;
        display: inline-block;
        margin-bottom: 12px;
        text-transform: uppercase;
        box-shadow: 0px 2px 8px rgba(15, 23, 42, 0.15);
    }

    /* 4. Assessment Card */
    div[data-testid="stForm"], div.stBlock {
        background-color: #FFFDF5 !important;
        border: 2px solid #FCD34D !important;
        border-radius: 16px !important;
        padding: 28px !important;
        box-shadow: 0px 8px 24px rgba(245, 158, 11, 0.08) !important;
        margin-top: 15px !important;
        margin-bottom: 20px !important;
    }

    /* 5. BLACK DROPDOWN BUTTON */
    .stSelectbox div[data-baseweb="select"],
    .stSelectbox div[data-baseweb="select"] > div,
    .stSelectbox div[data-baseweb="select"] > div:first-child,
    .stSelectbox div[data-baseweb="select"] [role="combobox"],
    .stSelectbox div[data-baseweb="select"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #0F172A !important;
        background: #0F172A !important;
        border: 1.5px solid #F59E0B !important;
        border-radius: 8px !important;
        min-height: 46px !important;
    }

    .stSelectbox div[data-baseweb="select"] *,
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] div,
    .stSelectbox div[data-baseweb="select"] [role="combobox"] * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    .stSelectbox div[data-baseweb="select"] svg {
        fill: #F59E0B !important;
    }

    /* 6. POPUP MENU CONTAINER */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"],
    div[role="listbox"] {
        background-color: #FFFDF5 !important;
        border: 2px solid #F59E0B !important;
        border-radius: 8px !important;
        padding: 6px !important;
        box-shadow: 0px 10px 25px rgba(15, 23, 42, 0.18) !important;
    }

    /* 7. DROPDOWN OPTIONS */
    ul[role="listbox"] li,
    li[role="option"] {
        background-color: #FEF3C7 !important;
        border: 1px solid #FDE68A !important;
        border-radius: 6px !important;
        margin-bottom: 4px !important;
        color: #78350F !important;
        -webkit-text-fill-color: #78350F !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 10px 14px !important;
    }

    ul[role="listbox"] li:hover,
    li[role="option"]:hover,
    li[aria-selected="true"] {
        background-color: #FDE68A !important;
        color: #451A03 !important;
        -webkit-text-fill-color: #451A03 !important;
    }

    /* 8. GOLD SUBMIT & ACTION BUTTONS */
    button[kind="primaryFormSubmit"],
    div[data-testid="stFormSubmitButton"] button,
    div.stButton > button {
        background-color: #F59E0B !important;
        background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%) !important;
        color: #0F172A !important;
        border-radius: 8px !important;
        border: 1px solid #D97706 !important;
        padding: 12px 24px !important;
        width: 100% !important;
        box-shadow: 0px 4px 14px rgba(245, 158, 11, 0.4) !important;
        transition: all 0.2s ease-in-out !important;
    }

    button[kind="primaryFormSubmit"] *,
    div[data-testid="stFormSubmitButton"] button *,
    div.stButton > button * {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 14px !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }

    /* WhatsApp Button */
    .wa-btn {
        display: block;
        text-align: center;
        background-color: #25D366;
        color: #FFFFFF !important;
        font-weight: 800;
        padding: 12px 16px;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 2px;
        text-transform: uppercase;
        font-size: 13px;
        letter-spacing: 0.5px;
    }
    .wa-btn:hover {
        background-color: #1EBE5D;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<span class="demo-badge">CRE8INTECH PROTOTYPE DEMO</span>', unsafe_allow_html=True)
st.title("📊 Financial Health Diagnostic Tool")
st.caption("Configured for **Money Wit Africa** (Founder: Oler Oladele, CFA)")
st.write("Complete this 2-minute assessment to receive your personalized Wealth Archetype score and recommended Money Wit roadmap.")

# Assessment Form (Module 1 & Lead Capture)
with st.form("diagnostic_form"):
    st.subheader("1. Your Profile & Contact Details")
    user_name = st.text_input("Full Name (or First Name)", placeholder="e.g. Amaka Adebayo")
    user_phone = st.text_input("WhatsApp Number", placeholder="e.g. +234 801 234 5678")
    
    st.subheader("2. Financial Health Assessment")
    earner_type = st.selectbox(
        "What best describes your current earning stage?",
        [
            "Early Career Professional", 
            "Mid-Level / Senior Professional", 
            "Business Owner / Entrepreneur", 
            "High-Net-Worth Individual"
        ]
    )
    
    primary_goal = st.selectbox(
        "What is your primary financial focus right now?",
        [
            "Building consistent monthly savings & emergency buffer", 
            "Investing in Eurobonds, FGN Sukuk & global equities", 
            "Clearing high-interest debt & cash flow optimization", 
            "Scaling and protecting a high-ticket wealth portfolio"
        ]
    )
    
    biggest_challenge = st.selectbox(
        "What is your biggest financial hurdle?",
        [
            "Financial jargon and investment complexity", 
            "Lack of time to analyze deals and market opportunities", 
            "Inconsistency in execution and accountability", 
            "Need for a vetted wealth circle and mastermind community"
        ]
    )
    
    submitted = st.form_submit_button("Generate My Wealth Roadmap 🚀")

# Module 2 & 3 Output
if submitted:
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        st.error("Please configure your OPENAI_API_KEY in Streamlit Secrets.")
    else:
        client = openai.OpenAI(api_key=api_key)
        
        display_name = user_name if user_name else "Investor"
        
        prompt = f"""
        Analyze this user for Money Wit Africa (Founder: Oler Oladele, CFA):
        - Name: {display_name}
        - Earner Stage: {earner_type}
        - Primary Goal: {primary_goal}
        - Biggest Hurdle: {biggest_challenge}

        OUTPUT FORMAT:
        1. **Wealth Archetype:** (A sharp, empowering title, e.g., 'The Strategic Wealth Builder')
        2. **Financial Diagnostics:** (2 structured bullet points analyzing their strengths and current gap)
        3. **Your 3-Pillar Action Roadmap:** (3 step-by-step tactical moves they need to make next)
        4. **Recommended Money Wit Program:** 
           - Match 'The Money Wit Club' for Eurobonds, asset scaling, and vetted deal circles.
           - Match 'The Money Wit School' for foundational budgeting, cashflow mastery, and habit loops.
           - Match 'Money Wit Bootcamps' for intensive short-term execution.
        """
        
        with st.spinner("Diagnosing your wealth profile..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            summary = response.choices[0].message.content
            
        st.success(f"Assessment Complete for {display_name}!")
        st.markdown("---")
        st.markdown(summary)

        # Module 3: Lead Dispatch & Action Links
        st.markdown("---")
        st.subheader("📥 Save & Share Your Wealth Roadmap")
        
        formatted_summary = (
            f"📊 *MONEY WIT AFRICA — FINANCIAL HEALTH DIAGNOSTIC*\n"
            f"👤 *Client:* {display_name}\n"
            f"📅 *Date:* {datetime.now().strftime('%d %b %Y')}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{summary}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✨ Empowered by The Money Wit Club (themoneywit.africa)"
        )
        
        encoded_wa = urllib.parse.quote(formatted_summary)
        wa_url = f"https://api.whatsapp.com/send?text={encoded_wa}"
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<a href="{wa_url}" target="_blank" class="wa-btn">📲 Share to WhatsApp</a>', unsafe_allow_html=True)
        with col2:
            st.download_button(
                label="📄 Download Roadmap (.txt)",
                data=formatted_summary,
                file_name=f"MoneyWit_Roadmap_{display_name.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
