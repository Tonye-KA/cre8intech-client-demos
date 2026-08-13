import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Financial Diagnostic | Money Wit Africa", 
    page_icon="📊", 
    layout="centered"
)

# Custom High-Contrast Styling (Yellow Page Background + Black Text)
st.markdown("""
    <style>
    /* Force Entire Page Background to Money Wit Vibrant Yellow */
    .stApp {
        background-color: #F59E0B !important;
    }

    /* Force Main Text to Bold Black/Navy */
    h1, h2, h3, p, span, label {
        color: #0F172A !important;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Cre8intech Badge - Sleek Navy Card with Gold Text */
    .demo-badge {
        background-color: #0F172A;
        color: #F59E0B !important;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        display: inline-block;
        margin-bottom: 12px;
    }

    /* Form Container - Clean White Card on Yellow Background */
    div[data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 2px solid #0F172A !important;
        border-radius: 16px !important;
        padding: 28px !important;
        box-shadow: 0px 8px 24px rgba(15, 23, 42, 0.15);
    }

    /* DROPDOWNS: Crisp White Container with Dark Navy Border & Text */
    div[data-baseweb="select"] > div {
        background-color: #F8FAFC !important;
        border: 2px solid #0F172A !important;
        border-radius: 10px !important;
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

    /* Dropdown Popup Menu List */
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

    /* ACTION BUTTON: Deep Navy Button with Bold White/Yellow Text */
    div.stButton > button {
        background-color: #0F172A !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 14px 24px !important;
        width: 100% !important;
        margin-top: 10px !important;
        box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.3) !important;
    }

    div.stButton > button * {
        color: #F59E0B !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
    }

    div.stButton > button:hover {
        background-color: #1E293B !important;
    }
    </style>
""", unsafe_allow_html=True)

# Restored Badge Header & Title
st.markdown('<span class="demo-badge">CRE8INTECH PROTOTYPE DEMO</span>', unsafe_allow_html=True)
st.title("📊 Financial Health Diagnostic Tool")
st.caption("Configured for **Money Wit Africa** (Founder: Oler Oladele, CFA)")
st.write("**Complete this 2-minute assessment to receive an instant financial health summary and discover your custom Money Wit roadmap.**")

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
        Analyze this user for Money Wit Africa:
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
