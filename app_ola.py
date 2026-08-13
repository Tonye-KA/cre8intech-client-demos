import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Financial Diagnostic | Money Wit Africa", 
    page_icon="📊", 
    layout="centered"
)

# Custom High-End Styling (Money Wit Gold & Deep Navy)
st.markdown("""
    <style>
    /* Main Background Force */
    .stApp {
        background-color: #0F172A !important;
    }

    /* Headings & Text */
    h1, h2, h3, p, span, label {
        color: #FFFFFF !important;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Cre8intech Badge */
    .demo-badge {
        background-color: #F59E0B;
        color: #0F172A !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        display: inline-block;
        margin-bottom: 12px;
    }

    /* Form Container */
    div[data-testid="stForm"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 16px !important;
        padding: 28px !important;
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.4);
    }

    /* MAKE DROPDOWNS POP: Gold Border, Dark Card, White Text */
    div[data-baseweb="select"] > div {
        background-color: #0F172A !important;
        border: 2px solid #F59E0B !important; /* Money Wit Logo Gold */
        border-radius: 10px !important;
        padding: 4px !important;
    }

    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Arrow icon inside dropdowns */
    div[data-baseweb="select"] svg {
        fill: #F59E0B !important;
    }

    /* Dropdown popup menu list */
    ul[role="listbox"] {
        background-color: #1E293B !important;
        border: 1px solid #F59E0B !important;
    }

    ul[role="listbox"] li {
        color: #FFFFFF !important;
        background-color: #1E293B !important;
    }

    ul[role="listbox"] li:hover {
        background-color: #F59E0B !important;
        color: #0F172A !important;
    }

    /* ACTION BUTTON: Eye-catching Logo Gold with Bold Dark Text */
    div.stButton > button {
        background-color: #F59E0B !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 14px 24px !important;
        width: 100% !important;
        margin-top: 10px !important;
        box-shadow: 0px 4px 15px rgba(245, 158, 11, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    div.stButton > button * {
        color: #0F172A !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
    }

    div.stButton > button:hover {
        background-color: #FFC107 !important;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# Restored Badge Header & Title
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
