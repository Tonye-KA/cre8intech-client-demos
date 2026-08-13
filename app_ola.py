import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Financial Diagnostic | Money Wit Africa", 
    page_icon="📊", 
    layout="centered"
)

# Custom High-End Styling (Clean White Page + Warm Soft Yellow Card Container)
st.markdown("""
    <style>
    /* 1. Force Page Background to Clean Modern White */
    .stApp {
        background-color: #FFFFFF !important;
    }

    /* 2. Headings & Typography */
    h1, h2, h3, p, span, label {
        color: #0F172A !important;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* 3. Cre8intech Demo Badge Header */
    .demo-badge {
        background-color: #0F172A;
        color: #F59E0B !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        display: inline-block;
        margin-bottom: 12px;
    }

    /* 4. Soft Warm Yellow Card Container for the Assessment */
    div[data-testid="stForm"] {
        background-color: #FFF9E6 !important; /* Elegant, soft Money Wit Yellow */
        border: 2px solid #FCD34D !important;  /* Warm golden border */
        border-radius: 16px !important;
        padding: 32px !important;
        box-shadow: 0px 8px 24px rgba(15, 23, 42, 0.06);
    }

    /* 5. DROPDOWNS: Crisp White Box with Dark Navy Border & Text */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1.5px solid #0F172A !important;
        border-radius: 8px !important;
        padding: 4px !important;
    }

    div[data-baseweb="select"] * {
        color: #0F172A !important;
        font-weight: 700 !important;
    }

    /* Arrow icon inside dropdowns */
    div[data-baseweb="select"] svg {
        fill: #0F172A !important;
    }

    /* Dropdown Popup Options Menu */
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 2px solid #0F172A !important;
    }

    ul[role="listbox"] li {
        color: #0F172A !important;
        background-color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    ul[role="listbox"] li:hover {
        background-color: #F59E0B !important;
        color: #0F172A !important;
    }

    /* 6. ACTION BUTTON: Eye-Catching Money Wit Gold with Bold Navy Text */
    div.stButton > button {
        background-color: #F59E0B !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 14px 24px !important;
        width: 100% !important;
        margin-top: 10px !important;
        box-shadow: 0px 4px 12px rgba(245, 158, 11, 0.3) !important;
    }

    div.stButton > button * {
        color: #0F172A !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
    }

    div.stButton > button:hover {
        background-color: #D97706 !important;
    }

    div.stButton > button:hover * {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# Badge Header & Title
st.markdown('<span class="demo-badge">CRE8INTECH PROTOTYPE DEMO</span>', unsafe_allow_html=True)
st.title("📊 Financial Health Diagnostic Tool")
st.caption("Configured for **Money Wit Africa** (Founder: Oler Oladele, CFA)")
st.write("Complete this 2-minute assessment to receive an instant financial health summary and discover your custom Money Wit roadmap.")

# Assessment Form inside Yellow Card
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
