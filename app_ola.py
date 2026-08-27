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

    /* Page Canvas */
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

    /* Typography */
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

    /* Demo Badge */
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

    /* Assessment Card */
    div[data-testid="stForm"], div.stBlock {
        background-color: #FFFDF5 !important;
        border: 2px solid #FCD34D !important;
        border-radius: 16px !important;
        padding: 28px !important;
        box-shadow: 0px 8px 24px rgba(245, 158, 11, 0.08) !important;
        margin-top: 15px !important;
        margin-bottom: 20px !important;
    }

    /* Dropdown Styling */
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

    /* Action Buttons */
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

    /* Custom Recommendation & Dispatch Cards */
    .rec-card {
        background-color: #FFFDF5;
        border: 1.5px solid #FCD34D;
        border-radius: 12px;
        padding: 18px;
        margin-top: 14px;
        margin-bottom: 14px;
    }

    .direct-link-btn {
        display: inline-block;
        background-color: #0F172A;
        color: #F59E0B !important;
        font-size: 13px;
        font-weight: 800;
        padding: 10px 18px;
        border-radius: 6px;
        text-decoration: none;
        margin-top: 8px;
        border: 1px solid #F59E0B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .direct-link-btn:hover {
        background-color: #F59E0B;
        color: #0F172A !important;
    }

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
st.write("Complete this 2-minute assessment to receive a customized action plan with direct pathway links.")

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

# Deterministic Catalog Routing
def get_exact_resources(goal, hurdle, stage):
    if "Eurobonds" in goal or "jargon" in hurdle:
        return {
            "title": "Fixed Income & Global Dollar Assets",
            "prod_name": "The Money Wit Community & Investment Advisory Circle",
            "prod_url": "https://themoneywit.africa/community/",
            "prod_desc": "Gain access to vetted Eurobond breakdowns, government debt instrument guides, and quarterly macro briefings.",
            "yt_topic": "Eurobonds vs Treasury Bills: Complete Beginner Guide",
            "yt_url": "https://www.youtube.com/@themoneywitclub/search?query=Eurobonds",
            "yt_desc": "Watch Oler Oladele break down how bond coupons work and how to safely purchase dollar fixed income without jargon."
        }
    elif "Multi-Asset" in goal or "vetted investment deals" in hurdle or "private wealth network" in hurdle or "High-Net-Worth" in stage:
        return {
            "title": "Private Deal Rooms & Multi-Asset Portfolio Scaling",
            "prod_name": "The Money Wit Club (Private Wealth Membership)",
            "prod_url": "https://themoneywit.africa/community/",
            "prod_desc": "An exclusive mastermind network for high earners to co-invest, evaluate private market opportunities, and access curated deals.",
            "yt_topic": "How High Earners Build Multi-Asset Portfolios",
            "yt_url": "https://www.youtube.com/@themoneywitclub/search?query=portfolio",
            "yt_desc": "Learn asset allocation strategies across cash, fixed income, real estate, and global equities."
        }
    elif "Business Owner" in stage:
        return {
            "title": "Entrepreneurial Wealth & Cash Flow Optimization",
            "prod_name": "The Money Wit Advisory & Wealth Planning",
            "prod_url": "https://themoneywit.africa/",
            "prod_desc": "Separate your company balance sheet from personal net worth and build disciplined profit-retention systems.",
            "yt_topic": "How Founders and Business Owners Pay Themselves First",
            "yt_url": "https://www.youtube.com/@themoneywitclub/search?query=business",
            "yt_desc": "A step-by-step masterclass on paying yourself a sustainable salary and building personal emergency assets."
        }
    else:
        return {
            "title": "Cashflow Foundations & Debt Elimination",
            "prod_name": "The Money Wit Financial Literacy & Budgeting Programs",
            "prod_url": "https://themoneywit.africa/",
            "prod_desc": "Master personal cashflow management, automate savings targets, and eliminate high-interest liabilities.",
            "yt_topic": "5 Practical Steps to Automate Your Monthly Savings",
            "yt_url": "https://www.youtube.com/@themoneywitclub/search?query=budgeting",
            "yt_desc": "Learn practical cash envelopes and automated banking structures to effortlessly save 20-30% of your income."
        }

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
            exact_res = get_exact_resources(primary_goal, biggest_challenge, earner_type)
            
            prompt = f"""
            You are the Senior Wealth Advisory Engine for Money Wit Africa (founded by Oler Oladele, CFA).
            Diagnose this specific user and generate a customized profile.

            USER PROFILE:
            - Client: {user_name}
            - Earning Stage: {earner_type}
            - Primary Focus: {primary_goal}
            - Primary Bottleneck: {biggest_challenge}
            - Recommended Focus Pathway: {exact_res['title']}

            STRICT OUTPUT INSTRUCTIONS:
            Format using clean Markdown:

            ### 🏆 Wealth Archetype: [Create a bold, empowering archetype title]

            #### 🔍 Financial Health Assessment:
            - **Current Positioning:** [1 sentence on their financial baseline]
            - **The Immediate Gap:** [1 sentence explaining how '{biggest_challenge}' directly restricts their goal of '{primary_goal}']

            #### 🚀 Immediate Tactical Action Steps:
            1. [Tactical Step 1 regarding cash management or savings automation]
            2. [Tactical Step 2 connecting them to their recommended learning track]
            """
            
            with st.spinner("Analyzing your profile and matching verified resources..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2
                )
                analysis_text = response.choices[0].message.content
                
            st.success(f"Personalized Action Plan Ready for {user_name}!")
            st.markdown("---")
            st.markdown(analysis_text)

            # Direct Verified Recommendation Cards
            st.markdown("---")
            st.subheader("🎯 Your Recommended Money Wit Pathways")
            
            col_rec1, col_rec2 = st.columns(2)
            with col_rec1:
                st.markdown(f"""
                <div class="rec-card">
                    <h4>🏛️ Recommended Program</h4>
                    <p style="font-weight: 700; color: #0F172A; font-size: 14.5px; margin-top: 4px;">{exact_res['prod_name']}</p>
                    <p style="font-size: 13px; color: #475569;">{exact_res['prod_desc']}</p>
                    <a href="{exact_res['prod_url']}" target="_blank" class="direct-link-btn">Access Program Page →</a>
                </div>
                """, unsafe_allow_html=True)
                
            with col_rec2:
                st.markdown(f"""
                <div class="rec-card">
                    <h4>📺 Free YouTube Masterclass</h4>
                    <p style="font-weight: 700; color: #0F172A; font-size: 14.5px; margin-top: 4px;">"{exact_res['yt_topic']}"</p>
                    <p style="font-size: 13px; color: #475569;">{exact_res['yt_desc']}</p>
                    <a href="{exact_res['yt_url']}" target="_blank" class="direct-link-btn">Watch Video on YouTube →</a>
                </div>
                """, unsafe_allow_html=True)

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
                f"{analysis_text}\n\n"
                f"🎯 *Recommended Program:* {exact_res['prod_name']}\n"
                f"🔗 *Direct Link:* {exact_res['prod_url']}\n\n"
                f"📺 *Free Masterclass:* {exact_res['yt_topic']}\n"
                f"▶️ *Watch Link:* {exact_res['yt_url']}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"✨ The Money Wit Club (themoneywit.africa)"
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
