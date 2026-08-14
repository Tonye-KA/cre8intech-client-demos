import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Financial Diagnostic | Money Wit Africa", 
    page_icon="📊", 
    layout="centered"
)

# Custom Styling (Money Wit Africa Brand: Rich Gold & Deep Slate/Onyx)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');

    /* 1. Page Background */
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
        color: #0F172A !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    p, span, label {
        color: #1E293B !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* 3. Cre8intech Demo Badge Header */
    .demo-badge {
        background-color: #0F172A !important;
        color: #F59E0B !important; /* Signature Money Wit Gold */
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

    /* 4. Warm Yellow Card Container */
    div[data-testid="stForm"], div.stBlock {
        background-color: #FFFDF5 !important;
        border: 2px solid #FCD34D !important;
        border-radius: 16px !important;
        padding: 32px !important;
        box-shadow: 0px 8px 24px rgba(245, 158, 11, 0.08) !important;
        margin-bottom: 20px !important;
    }

    /* 5. DROPDOWN POPUP MENU (CRISP HIGH-CONTRAST VISIBLE TEXT) */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"],
    div[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #F59E0B !important;
        border-radius: 8px !important;
        box-shadow: 0px 10px 25px rgba(15, 23, 42, 0.15) !important;
    }

    /* Force all option items and text to be bold, dark, and clear */
    ul[role="listbox"] li,
    ul[role="listbox"] li *,
    div[data-baseweb="menu"] div,
    div[data-baseweb="menu"] span,
    div[data-baseweb="popover"] span,
    div[data-baseweb="popover"] div {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        opacity: 1 !important;
    }

    /* Hover State inside Dropdown */
    ul[role="listbox"] li:hover,
    ul[role="listbox"] li:hover *,
    div[data-baseweb="menu"] div:hover,
    [aria-selected="true"] {
        background-color: #FEF3C7 !important;
        color: #92400E !important;
        -webkit-text-fill-color: #92400E !important;
    }

    /* 6. SIGNATURE MONEY WIT GOLDEN BUTTON */
    div.stButton > button,
    button[kind="primaryFormSubmit"],
    button[kind="secondaryFormSubmit"],
    button[data-testid="stFormSubmitButton"] > button {
        background-color: #F59E0B !important;
        background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%) !important;
        border-radius: 8px !important;
        border: 1px solid #D97706 !important;
        padding: 14px 24px !important;
        width: 100% !important;
        margin-top: 12px !important;
        box-shadow: 0px 4px 14px rgba(245, 158, 11, 0.35) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button *,
    button[kind="primaryFormSubmit"] *,
    button[data-testid="stFormSubmitButton"] > button * {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 15px !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }

    div.stButton > button:hover,
    button[kind="primaryFormSubmit"]:hover,
    button[data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0px 6px 18px rgba(245, 158, 11, 0.45) !important;
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
