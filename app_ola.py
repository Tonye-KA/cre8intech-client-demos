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
        max-width: 740px !important;
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

    label[data-testid="stWidgetLabel"] p {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 14.5px !important;
    }

    /* 3. Demo Badge */
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

    /* 5. Dropdown Styling */
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

    /* 6. Dropdown Options Menu */
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

    /* 7. Action Buttons */
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

    /* Custom Action Links */
    .dispatch-btn-wa {
        display: block;
        text-align: center;
        background-color: #25D366;
        color: #FFFFFF !important;
        font-weight: 800;
        padding: 12px 14px;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 4px;
        text-transform: uppercase;
        font-size: 13px;
        letter-spacing: 0.5px;
    }
    .dispatch-btn-wa:hover {
        background-color: #1EBE5D;
        color: #FFFFFF !important;
    }

    .dispatch-btn-email {
        display: block;
        text-align: center;
        background-color: #0F172A;
        color: #F59E0B !important;
        font-weight: 800;
        padding: 12px 14px;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 4px;
        text-transform: uppercase;
        font-size: 13px;
        letter-spacing: 0.5px;
        border: 1px solid #F59E0B;
    }
    .dispatch-btn-email:hover {
        background-color: #1E293B;
        color: #FBBF24 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<span class="demo-badge">CRE8INTECH PROTOTYPE DEMO</span>', unsafe_allow_html=True)
st.title("📊 Financial Health Diagnostic Tool")
st.caption("Configured for **Money Wit Africa** (Founder: Oler Oladele, CFA)")
st.write("Complete this 2-minute assessment to receive a customized action plan mapped to the Money Wit ecosystem.")

# Assessment Form
with st.form("diagnostic_form"):
    st.subheader("1. Your Details")
    user_name = st.text_input("Full Name *", placeholder="e.g. Amaka Adebayo")
    user_email = st.text_input("Email Address *", placeholder="e.g. amaka@example.com")
    user_phone = st.text_input("WhatsApp Number (Optional)", placeholder="e.g. +234 801 234 5678")
    
    st.subheader("2. Financial Health Assessment")
    earner_type = st.selectbox(
        "What best describes your current career / earning stage?",
        [
            "Early Career Professional (Building foundation & monthly saving habits)", 
            "Mid-Level / Senior Professional (Surplus cash looking for high-yield passive returns)", 
            "Business Owner / Entrepreneur (Managing business cashflow & personal wealth)", 
            "High-Net-Worth Individual (Preserving capital, hedging inflation & dollar assets)"
        ]
    )
    
    primary_goal = st.selectbox(
        "What is your primary financial focus right now?",
        [
            "Building a 6-Month Emergency Buffer & Strict Monthly Budget", 
            "Investing in Eurobonds, FGN Sukuk & Global Dollar Fixed Income", 
            "Clearing High-Interest Debts & Structuring Cashflow Habits", 
            "Scaling a Multi-Asset Investment Portfolio & Accessing Private Deals"
        ]
    )
    
    biggest_challenge = st.selectbox(
        "What is your biggest financial hurdle?",
        [
            "Confused by financial jargon and complex market terminology", 
            "Lack of time to research and analyze vetted investment deals", 
            "Inconsistency in execution, impulse spending, and lack of budgeting structure", 
            "Need for a high-caliber private wealth network and live accountability"
        ]
    )
    
    submitted = st.form_submit_button("Generate My Action Plan 🚀")

# Process Diagnostic
if submitted:
    if not user_name.strip():
        st.error("Please provide your full name.")
    elif not user_email.strip() or "@" not in user_email:
        st.error("Please provide a valid email address.")
    else:
        api_key = st.secrets.get("OPENAI_API_KEY", "")
        if not api_key:
            st.error("Please configure your OPENAI_API_KEY in Streamlit Secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            
            prompt = f"""
            You are the Senior Wealth Advisory Engine for Money Wit Africa (founded by Oler Oladele, CFA).
            Diagnose this specific user and select the EXACT MATCHING product, masterclass, and YouTube masterclass from the verified catalog below.

            USER PROFILE:
            - Name: {user_name}
            - Earning Stage: {earner_type}
            - Primary Goal: {primary_goal}
            - Primary Hurdle: {biggest_challenge}

            OFFICIAL MONEY WIT CATALOG & TAXONOMY (STRICT MAPPING RULES):
            Rule 1: If Goal involves "Eurobonds, FGN Sukuk & Global Dollar Fixed Income" OR Hurdle is "Confused by financial jargon":
               -> Primary Solution: 'The Fixed Income & Eurobond Mastery Masterclass'
               -> URL: https://themoneywit.africa/
               -> YouTube: "Eurobonds vs Treasury Bills: How to Invest Safely in Dollars" (https://www.youtube.com/@themoneywitclub)
               -> Solve Angle: Demystifies bond yields, interest rate cycles, and dollar preservation without confusing jargon.

            Rule 2: If Goal involves "Scaling a Multi-Asset Investment Portfolio" OR Hurdle is "Lack of time to research deals" OR "Need for private wealth network":
               -> Primary Solution: 'The Money Wit Club (Exclusive Wealth Membership)'
               -> URL: https://themoneywit.africa/community/
               -> YouTube: "How High-Earning Professionals Structure Multi-Asset Portfolios" (https://www.youtube.com/@themoneywitclub)
               -> Solve Angle: Hands-off curated deal analysis, monthly investor briefings, and a private circle of peer investors.

            Rule 3: If Goal involves "Building Emergency Buffer" OR "Clearing High-Interest Debts" OR Hurdle is "Inconsistency & lack of budgeting structure":
               -> Primary Solution: 'The Money Wit School: Cashflow & Wealth Foundations Course'
               -> URL: https://themoneywit.africa/
               -> YouTube: "5 Practical Steps to Automate Your Savings and Build a 6-Month Buffer" (https://www.youtube.com/@themoneywitclub)
               -> Solve Angle: Provides automated cashflow blueprints, debt repayment ladders, and habit-tracking loops.

            Rule 4: If Earning Stage is "Business Owner / Entrepreneur":
               -> Primary Solution: 'The Money Wit Masterclass: Business Finance & Personal Wealth Separation'
               -> URL: https://themoneywit.africa/
               -> YouTube: "How Founders and Business Owners Pay Themselves and Build Personal Assets" (https://www.youtube.com/@themoneywitclub)
               -> Solve Angle: Solves the co-mingling of funds and turns business profits into diversified personal wealth.

            OUTPUT FORMAT (Strict Markdown):

            ### 🏆 Wealth Archetype: [Specific empowering title, e.g., 'The Dollar Asset Strategist' or 'The Scalable Portfolio Builder']

            #### 🔍 Financial Health Assessment:
            - **Current Position:** [1 sentence on their financial positioning and readiness]
            - **The Bottleneck:** [1 sentence explaining how '{biggest_challenge}' directly restricts their goal of '{primary_goal}']

            #### 🎯 Your Recommended Money Wit Solution:
            - **Primary Program / Masterclass:** [Use the EXACT matched program name from the rules]
            - **Direct Access Link:** [[Access This Program on Money Wit Africa](URL_from_rule)]
            - **Why This Solves Your Hurdle:** [2 sentences detailing how this exact program addresses '{biggest_challenge}' and accomplishes '{primary_goal}']

            #### 📺 Recommended Free Video Masterclass:
            - **YouTube Topic:** "[Exact YouTube Video Title from rule]"
            - **Watch Link:** [[Watch Episode on 'The Money Wit Show' YouTube](YouTube_URL_from_rule)]
            - **Core Takeaway:** [1 concise sentence on what they will master from this episode]

            #### 🚀 Immediate Tactical Action Steps:
            1. [Tactical Step 1 specific to their immediate cash or asset move]
            2. [Tactical Step 2 directly connecting them to the recommended Money Wit pathway]
            """
            
            with st.spinner("Analyzing your profile and matching optimal pathways..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2
                )
                summary = response.choices[0].message.content
                
            st.success(f"Personalized Action Plan Ready for {user_name}!")
            st.markdown("---")
            st.markdown(summary)

            # Dispatch Options
            st.markdown("---")
            st.subheader("📤 Save or Share Your Action Plan")
            st.write("Send this diagnostic summary directly to your Email or WhatsApp for easy reference:")
            
            full_roadmap_text = (
                f"📊 *MONEY WIT AFRICA — PERSONALIZED ACTION PLAN*\n"
                f"👤 *Client:* {user_name}\n"
                f"📧 *Email:* {user_email}\n"
                f"📅 *Date:* {datetime.now().strftime('%d %b %Y')}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{summary}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"✨ Access your recommended program: https://themoneywit.africa\n"
                f"📺 Watch 'The Money Wit Show' on YouTube: https://www.youtube.com/@themoneywitclub"
            )
            
            # WhatsApp Link
            encoded_wa = urllib.parse.quote(full_roadmap_text)
            wa_share_url = f"https://api.whatsapp.com/send?text={encoded_wa}"
            
            # Email Mailto Link
            email_subject = urllib.parse.quote(f"My Money Wit Action Plan - {user_name}")
            email_body = urllib.parse.quote(full_roadmap_text)
            mailto_url = f"mailto:{user_email}?subject={email_subject}&body={email_body}"

            col_send1, col_send2 = st.columns(2)
            with col_send1:
                st.markdown(f'<a href="{wa_share_url}" target="_blank" class="dispatch-btn-wa">📲 Send / Share via WhatsApp</a>', unsafe_allow_html=True)
            with col_send2:
                st.markdown(f'<a href="{mailto_url}" target="_blank" class="dispatch-btn-email">✉️ Send to My Email</a>', unsafe_allow_html=True)
