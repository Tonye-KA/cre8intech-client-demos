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

    /* Custom Dispatch Buttons */
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
st.write("Complete this 2-minute free assessment to know your financial health and receive a customized action plan")

# Delivery Preference Selector (Controls dynamic contact requirement in Step 3)
st.markdown("**Select Your Report Delivery Preference:**")
delivery_choice = st.radio(
    "Choose how you want to receive and access your report:",
    ["📲 Send via WhatsApp", "✉️ Send via Email", "📄 Download Report (PDF / Text)"],
    horizontal=True,
    label_visibility="collapsed"
)

# Assessment Form
with st.form("diagnostic_form"):
    # Step 1: Name Only
    st.subheader("1. Your Details")
    user_name = st.text_input("Full Name *", placeholder="e.g. Amaka Adebayo")
    
    # Step 2: Dropdowns
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
    
    # Step 3: Contact Details based on Delivery Choice
    st.subheader("3. Report Delivery Details")
    if "WhatsApp" in delivery_choice:
        user_phone = st.text_input("WhatsApp Number *", placeholder="e.g. +234 801 234 5678")
        user_email = ""
    elif "Email" in delivery_choice:
        user_email = st.text_input("Email Address *", placeholder="e.g. amaka@example.com")
        user_phone = ""
    else:
        st.info("📄 Your customized report will be generated on-screen with an instant download button.")
        user_phone = ""
        user_email = ""
    
    submitted = st.form_submit_button("Generate & Access My Action Plan 🚀")

# Diagnostic Processing & Validation
if submitted:
    if not user_name.strip():
        st.error("Please provide your full name in Step 1.")
    elif "WhatsApp" in delivery_choice and not user_phone.strip():
        st.error("Please enter your WhatsApp Number in Step 3 to receive your report.")
    elif "Email" in delivery_choice and (not user_email.strip() or "@" not in user_email):
        st.error("Please enter a valid Email Address in Step 3 to receive your report.")
    else:
        api_key = st.secrets.get("OPENAI_API_KEY", "")
        if not api_key:
            st.error("Please configure your OPENAI_API_KEY in Streamlit Secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            
            contact_info = user_phone if "WhatsApp" in delivery_choice else (user_email if "Email" in delivery_choice else "Direct Download")
            
            prompt = f"""
            You are the Senior Wealth Advisory Engine for Money Wit Africa (founded by Oler Oladele, CFA).
            Diagnose this specific user and format a personalized output that ALWAYS includes The Money Wit Club along with their specific pathway.

            USER PROFILE:
            - Name: {user_name}
            - Contact: {contact_info} ({delivery_choice})
            - Earning Stage: {earner_type}
            - Primary Goal: {primary_goal}
            - Primary Hurdle: {biggest_challenge}

            OFFICIAL DESTINATIONS:
            - The Money Wit Club: https://themoneywit.africa/community/
            - The Money Wit School: https://school.themoneywit.africa/
            - Strategy & Solutions: https://themoneywit.africa/what-we-do/
            - YouTube Channel: https://www.youtube.com/@oleroladele

            MAPPING RULES:
            Rule 1 (Eurobonds / Jargon):
               - Specific Program: 'The Money Wit Club (Fixed Income & Deals Track)'
               - Program URL: https://themoneywit.africa/community/
               - YouTube Video Title: "Invest in Nigeria from the Diaspora: Dollar-Denominated Opportunities & High Returns"
               - YouTube URL: https://www.youtube.com/@oleroladele
               - Explanation: Breaks down foreign exchange risk, bond yields, and capital preservation without confusing jargon.

            Rule 2 (Multi-Asset / Time / Network):
               - Specific Program: 'The Money Wit Club (Private Wealth Community)'
               - Program URL: https://themoneywit.africa/community/
               - YouTube Video Title: "Don't Buy Stocks in 2026 Until You Watch This"
               - YouTube URL: https://www.youtube.com/@oleroladele
               - Explanation: Provides hands-off curated deal analysis, monthly briefings, and a private circle of peer investors.

            Rule 3 (Emergency Buffer / Debt / Budgeting):
               - Specific Program: 'The Money Wit School (Foundation Path) + The Money Wit Club'
               - Program URL: https://school.themoneywit.africa/
               - YouTube Video Title: "Personal Finance for Beginners: 7 Things You Should Know"
               - YouTube URL: https://www.youtube.com/@oleroladele
               - Explanation: Equips you with automated cashflow blueprints, debt elimination ladders, and accountability loops.

            Rule 4 (Business Owner):
               - Specific Program: 'The Money Wit High Earner Clarity Program + The Money Wit Club'
               - Program URL: https://themoneywit.africa/what-we-do/
               - YouTube Video Title: "How Compounding Can Help You Double Your Money"
               - YouTube URL: https://www.youtube.com/@oleroladele
               - Explanation: Separates business and personal cashflow to build sustainable, long-term personal assets.

            OUTPUT FORMAT (Strict Markdown):

            ### 🏆 Wealth Archetype: [Specific empowering title, e.g., 'The Strategic Asset Builder']

            #### 🔍 Financial Health Assessment:
            - **Current Position:** [1 crisp sentence on their readiness]
            - **The Bottleneck:** [1 crisp sentence explaining how '{biggest_challenge}' directly restricts their goal of '{primary_goal}']

            #### 🎯 Your Recommended Money Wit Solution:
            - **Primary Program:** [Use the program name from the matched rule]
            - **Direct Access Link:** [[Access Program & Registration]](Program_URL_from_rule)
            - **Core Wealth Community:** [[Join The Money Wit Club]](https://themoneywit.africa/community/) (Essential for ongoing accountability, deal access, and investor mastermind circles)
            - **Why This Solves Your Hurdle:** [2 sentences detailing how this combination eliminates '{biggest_challenge}' and achieves '{primary_goal}']

            #### 📺 Recommended Free Video Masterclass:
            - **YouTube Masterclass:** "[Exact YouTube Video Title from rule]"
            - **Watch Link:** [[Watch Episode on Oler Oladele's YouTube Channel]](YouTube_URL_from_rule)
            - **Core Takeaway:** [1 sentence on what they will master from this episode]

            #### 🚀 Immediate Tactical Action Steps:
            1. [Tactical Step 1 specific to their immediate savings/budgeting/portfolio move]
            2. **Enroll in your matched path:** Explore [[Program Name]](Program_URL_from_rule) to build structured financial systems.
            3. **Get continuous accountability:** Apply to [[The Money Wit Club]](https://themoneywit.africa/community/) to join fellow investors and access curated deal flow.
            4. **Start learning immediately:** Watch [[Episode: YouTube Video Title]](YouTube_URL_from_rule) for practical guidance.
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

            # Targeted Dispatch Action matching chosen delivery channel
            st.markdown("---")
            st.subheader("📤 Confirm Delivery of Your Action Plan")
            
            full_roadmap_text = (
                f"📊 MONEY WIT AFRICA — PERSONALIZED ACTION PLAN\n"
                f"👤 Client: {user_name}\n"
                f"📞 Delivery Channel: {delivery_choice}\n"
                f"📅 Date: {datetime.now().strftime('%d %b %Y')}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{summary}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"✨ Access The Money Wit Club: https://themoneywit.africa/community/\n"
                f"📺 Watch 'The Money Wit' on YouTube: https://www.youtube.com/@oleroladele"
            )
            
            if "WhatsApp" in delivery_choice:
                encoded_wa = urllib.parse.quote(full_roadmap_text)
                wa_share_url = f"https://api.whatsapp.com/send?text={encoded_wa}"
                st.write(f"Click below to receive and open this roadmap directly on WhatsApp:")
                st.markdown(f'<a href="{wa_share_url}" target="_blank" class="dispatch-btn-wa">📲 Open & Send Report via WhatsApp</a>', unsafe_allow_html=True)
            elif "Email" in delivery_choice:
                email_subject = urllib.parse.quote(f"My Money Wit Action Plan - {user_name}")
                email_body = urllib.parse.quote(full_roadmap_text)
                mailto_url = f"mailto:{user_email}?subject={email_subject}&body={email_body}"
                st.write(f"Click below to send this roadmap to your email inbox ({user_email}):")
                st.markdown(f'<a href="{mailto_url}" target="_blank" class="dispatch-btn-email">✉️ Open & Send to My Email</a>', unsafe_allow_html=True)
            else:
                st.write("Click below to download your complete diagnostic summary sheet:")
                st.download_button(
                    label="📄 Download Full Action Plan Report (.txt / PDF-ready)",
                    data=full_roadmap_text,
                    file_name=f"MoneyWit_Action_Plan_{user_name.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
