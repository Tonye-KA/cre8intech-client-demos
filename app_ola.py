import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Financial Diagnostic | Money Wit Africa", 
    page_icon="📊", 
    layout="centered"
)

# Custom Styling (Uniform Warm Cream Dropdown Options & Money Wit Gold Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');

    /* 1. Page Background & Padding */
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

    /* 2. Headings & Body Text */
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

    /* Form Question Labels */
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

    /* 4. Warm Yellow Assessment Card */
    div[data-testid="stForm"], div.stBlock {
        background-color: #FFFDF5 !important;
        border: 2px solid #FCD34D !important;
        border-radius: 16px !important;
        padding: 28px !important;
        box-shadow: 0px 8px 24px rgba(245, 158, 11, 0.08) !important;
        margin-top: 15px !important;
        margin-bottom: 20px !important;
    }

    /* 5. SELECTBOX INPUT CONTAINER */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1.5px solid #F59E0B !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] * {
        color: #0F172A !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="select"] svg {
        fill: #D97706 !important;
    }

    /* 6. POPUP MENU CONTAINER */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"],
    div[role="listbox"] {
        background-color: #FFFDF5 !important;
        border: 2px solid #F59E0B !important;
        border-radius: 8px !important;
        padding: 4px !important;
        box-shadow: 0px 10px 25px rgba(245, 158, 11, 0.2) !important;
    }

    /* 7. MAKE ALL DROPDOWN OPTIONS HAVE THE WARM CREAM CARD BACKGROUND & BOLD BROWN TEXT */
    ul[role="listbox"] li,
    ul[role="listbox"] > li,
    li[role="option"],
    div[role="option"],
    div[data-baseweb="menu"] div,
    div[data-baseweb="popover"] li {
        background-color: #FEF3C7 !important; /* Uniform Warm Cream */
        border: 1px solid #FDE68A !important;
        border-radius: 6px !important;
        margin-bottom: 4px !important;
        color: #78350F !important; /* Bold Golden Brown */
        -webkit-text-fill-color: #78350F !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 10px 14px !important;
        opacity: 1 !important;
    }

    /* Target inner spans/divs inside every option */
    ul[role="listbox"] li *,
    li[role="option"] *,
    div[role="option"] * {
        color: #78350F !important;
        -webkit-text-fill-color: #78350F !important;
        font-weight: 700 !important;
    }

    /* Hover & Active Highlight */
    ul[role="listbox"] li:hover,
    ul[role="listbox"] li:hover *,
    li[role="option"]:hover,
    li[role="option"]:hover *,
    li[aria-selected="true"],
    li[aria-selected="true"] * {
        background-color: #FDE68A !important; /* Richer Amber on Hover */
        color: #451A03 !important;
        -webkit-text-fill-color: #451A03 !important;
    }

    /* 8. BRIGHT MONEY WIT GOLD BUTTON */
    button[kind="primaryFormSubmit"],
    button[kind="secondaryFormSubmit"],
    button[data-testid="baseButton-primary"],
    button[data-testid="baseButton-secondary"],
    div[data-testid="stFormSubmitButton"] button,
    div.stButton > button {
        background-color: #F59E0B !important;
        background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%) !important;
        color: #0F172A !important;
        border-radius: 8px !important;
        border: 1px solid #D97706 !important;
        padding: 14px 28px !important;
        width: auto !important;
        min-width: 260px !important;
        margin-top: 14px !important;
        box-shadow: 0px 4px 14px rgba(245, 158, 11, 0.4) !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* Force button text to bold black */
    button[kind="primaryFormSubmit"] *,
    button[kind="secondaryFormSubmit"] *,
    button[data-testid="baseButton-primary"] *,
    button[data-testid="baseButton-secondary"] *,
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

    button[kind="primaryFormSubmit"]:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0px 6px 18px rgba(245, 158, 11, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<span class="demo-badge">CRE8INTECH PROTOTYPE DEMO</span>', unsafe_allow_html=True)
st.title("📊 Financial Health Diagnostic Tool")
st.caption("Configured for **Money Wit Africa** (Founder: Oler Oladele, CFA)")
st.write("Complete this 2-minute assessment to receive an instant financial health summary and discover your custom Money Wit roadmap.")

# Assessment Form
with st.form("diagnostic_form"):
    earner_type = st.selectbox(
        "1. What best describes your current career / earning stage?",
        [
            "Early Career Professional", 
            "Mid-Level / Senior Professional", 
            "Business Owner / Entrepreneur", 
            "High-Net-Worth Individual"
        ]
    )
    
    primary_goal = st.selectbox(
        "2. What is your primary financial focus right now?",
        [
            "Building consistent monthly savings habits", 
            "Investing in Eurobonds & global equities", 
            "Clearing high-interest debt & budgeting", 
            "Scaling an investment portfolio"
        ]
    )
    
    biggest_challenge = st.selectbox(
        "3. What is your biggest financial hurdle?",
        [
            "Financial jargon is confusing", 
            "Lack of time to analyze deals", 
            "Inconsistency in execution", 
            "Need a vetted community & accountability"
        ]
    )
    
    submitted = st.form_submit_button("Generate Financial Profile 🚀", type="primary")

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
