import streamlit as st
import openai

# Page Setup
st.set_page_config(page_title="Financial Diagnostic | Money Wit Africa", page_icon="📊", layout="centered")

# Custom Brand Styling (Money Wit Africa Palette - Complete Dropdown Styling)
st.markdown("""
    <style>
    /* Force page background */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }
    
    /* Typography */
    h1, h2, h3, p, span, label, div {
        color: #0F172A !important;
        font-family: 'Georgia', serif;
    }

    /* FORCE ALL DROPDOWN CONTAINERS TO BE GOLD/YELLOW WITH BLACK TEXT */
    div[data-baseweb="select"], 
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] * {
        background-color: #F59E0B !important; /* Money Wit Gold/Yellow */
        color: #000000 !important;             /* Bold Black Text */
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
    }

    /* Force text inside the selected option box */
    div[data-baseweb="select"] div[role="button"] {
        color: #000000 !important;
    }

    /* Force dropdown arrow icon to be black */
    div[data-baseweb="select"] svg {
        fill: #000000 !important;
        color: #000000 !important;
    }

    /* DROPDOWN POPUP MENU (LIST OF OPTIONS) */
    ul[role="listbox"],
    div[data-baseweb="menu"] {
        background-color: #F59E0B !important;
    }
    
    ul[role="listbox"] li,
    div[data-baseweb="menu"] div {
        color: #000000 !important;
        background-color: #F59E0B !important;
        font-weight: 600 !important;
    }

    /* Hover effect on dropdown items */
    ul[role="listbox"] li:hover,
    div[data-baseweb="menu"] div:hover {
        background-color: #D97706 !important; /* Deeper gold on hover */
        color: #FFFFFF !important;
    }

    /* SUBMIT BUTTON: Match Brand Styling */
    div.stButton > button {
        background-color: #0F172A !important; /* Deep Navy Button */
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 20px !important;
        width: 100% !important;
    }

    div.stButton > button * {
        color: #F59E0B !important; /* Gold Text on Navy Button */
        font-size: 16px !important;
        font-weight: 800 !important;
    }

    div.stButton > button:hover {
        background-color: #D97706 !important;
    }

    div.stButton > button:hover * {
        color: #FFFFFF !important;
    }

    /* Demo Badge Header */
    .demo-badge {
        background-color: #0F172A;
        color: #F59E0B !important;
        padding: 6px 14px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<span class="demo-badge">CRE8INTECH PROTOTYPE DEMO</span>', unsafe_allow_html=True)
st.title("📊 Financial Health Diagnostic Tool")
st.caption("Configured for **Money Wit Africa**")

st.write("Complete this 2-minute assessment to receive an instant financial health summary and discover your custom Money Wit roadmap.")

with st.form("diagnostic_form"):
    earner_type = st.selectbox(
        "1. Current career / earning stage:",
        ["Early Career Professional", "Mid-Level / Senior Professional", "Business Owner / Entrepreneur", "High-Net-Worth Individual"]
    )
    
    primary_goal = st.selectbox(
        "2. Primary financial goal right now:",
        ["Building consistent monthly savings habits", "Investing in Eurobonds & global equities", "Clearing high-interest debt & budgeting", "Scaling an investment portfolio"]
    )
    
    biggest_challenge = st.selectbox(
        "3. Biggest financial hurdle:",
        ["Financial jargon is confusing", "Lack of time to analyze deals", "Inconsistency in execution", "Need a vetted community & accountability"]
    )
    
    submitted = st.form_submit_button("Generate Financial Profile 🚀")

if submitted:
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        st.error("Please add your API Key in Streamlit Secrets.")
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
        
        with st.spinner("Analyzing profile..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            summary = response.choices[0].message.content
            
        st.success("Analysis Complete!")
        st.markdown("---")
        st.markdown(summary)
