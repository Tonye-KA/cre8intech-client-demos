import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Financial Diagnostic | Money Wit Africa", 
    page_icon="📊", 
    layout="centered"
)

# Custom High-End Styling (Money Wit Africa Emerald & Wealth Gold Palette)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');

    /* 1. Page Background to Clean Modern White */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #0F172A !important;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* 2. Headings & Typography */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #064E3B !important; /* Deep Money Wit Emerald */
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    p, span, label {
        color: #1E293B !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* 3. Cre8intech Demo Badge Header */
    .demo-badge {
        background-color: #064E3B !important;
        color: #FCD34D !important; /* Gold Accent */
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.2px;
        display: inline-block;
        margin-bottom: 12px;
        text-transform: uppercase;
        box-shadow: 0px 2px 8px rgba(6, 78, 59, 0.2);
    }

    /* 4. Elegant Soft Emerald-Tinted Card Container */
    div[data-testid="stForm"], div.stBlock {
        background-color: #F0FDF4 !important; /* Soft Luxury Wealth Tint */
        border: 1.5px solid #A7F3D0 !important;  /* Refined Mint-Emerald Border */
        border-radius: 16px !important;
        padding: 32px !important;
        box-shadow: 0px 8px 24px rgba(6, 78, 59, 0.06) !important;
        margin-bottom: 20px !important;
    }

    /* 5. DROPDOWNS: Crisp White Container with Dark Slate Text */
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        width: 100% !important;
        margin-bottom: 4px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1.5px solid #059669 !important; /* Emerald Border */
        border-radius: 8px !important;
        padding: 2px 8px !important;
        min-height: 44px !important;
    }

    div[data-baseweb="select"] * {
        color: #0F172A !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    div[data-baseweb="select"] svg {
        fill: #047857 !important;
    }

    /* Dropdown Popup Options Menu */
    ul[role="listbox"],
    div[data-baseweb="menu"],
    div[data-baseweb="popover"],
    div[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #059669 !important;
        border-radius: 8px !important;
    }

    ul[role="listbox"] li,
    div[data-baseweb="menu"] div,
    div[data-baseweb="popover"] div {
        color: #0F172A !important;
        background-color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
    }

    ul[role="listbox"] li:hover,
    div[data-baseweb="menu"] div:hover,
    div[data-baseweb="popover"] div:hover {
        background-color: #ECFDF5 !important;
        color: #047857 !important;
    }

    /* 6. ACTION BUTTON: Money Wit Emerald with High-Contrast White Text */
    div.stButton > button,
    button[kind="primaryFormSubmit"],
    button[kind="secondaryFormSubmit"],
    button[data-testid="stFormSubmitButton"] > button {
        background-color: #047857 !important; /* Wealth Emerald */
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 14px 24px !important;
        width: 100% !important;
        margin-top: 12px !important;
        box-shadow: 0px 4px 14px rgba(4, 120, 87, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button *,
    button[kind="primaryFormSubmit"] *,
    button[data-testid="stFormSubmitButton"] > button * {
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 15px !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }

    div.stButton > button:hover,
    button[kind="primaryFormSubmit"]:hover,
    button[data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, #047857 0%, #064E3B 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0px 6px 18px rgba(4, 120, 87, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Badge Header & Title
st.markdown('<span class="demo-badge">CRE8INTECH PROTOTYPE DEMO</span>', unsafe_allow_html=True)
st.title("📊 Financial Health Diagnostic Tool")
st.caption("Configured for **Money Wit Africa** (Founder: Oler Oladele, CFA)")
st.write("Complete this 2-minute assessment to receive an instant financial health summary and discover your custom Money Wit roadmap.")

# Assessment Form
with st.form("diagnostic_form"):
    earner_type = st.selectbox(
        "1. What best describes your current career / earning stage?",
        ["Early Career Professional", "Mid-Level / Senior Professional", "Business Owner / Entrepreneur", "High-Net-Worth Individual"]
    )
    
    primary_goal = st.selectbox(
        "2. What is your primary financial focus right now?",
        ["Building consistent monthly savings habits", "Investing in Eurobonds & global equities", "Clearing high-interest debt & budgeting", "Scaling an investment portfolio"]
    )
    
    biggest_challenge = st.selectbox(
        "3. What is your biggest financial hurdle?",
        ["Financial jargon is confusing", "Lack of time to analyze deals", "Inconsistency in execution", "Need a vetted community & accountability"]
    )
    
    submitted = st.form_submit_button("Generate Financial Profile 🚀")

if submitted:
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        st.error("Please add your OPENAI_API_KEY in Streamlit Secrets.")
    else:
        client = openai.OpenAI(api_key=api_key)
        
        prompt = f"""
        Analyze this user for Money Wit Africa (Founder: Oler Oladele, CFA):
        - Earner Stage: {earner_type}
        - Primary Goal: {primary_goal}
        - Biggest Hurdle: {biggest_challenge}

        OUTPUT FORMAT:
        1. **Profile Title:** (A bold 1-line title, e.g., 'The Wealth-Building Strategist')
        2. **Key Insights:** (2 bullet points with professional, warm, encouraging analysis)
        3. **Recommended Program:** 
           - Recommend 'The Money Wit Club' if interested in Eurobonds, high net worth tools, or deal analysis.
           - Recommend 'The Money Wit School' if focusing on habits, budgeting, or foundation building.
           - Recommend 'Money Wit Bootcamps' if seeking short, intensive financial alignment.
        4. **Next Steps:** Clear call to action to join the platform.
        """
        
        with st.spinner("Analyzing your financial health profile..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            summary = response.choices[0].message.content
            
        st.success("Analysis Complete!")
        st.markdown("---")
        st.markdown(summary)
