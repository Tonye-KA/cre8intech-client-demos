import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Financial Diagnostic | Money Wit Africa", 
    page_icon="📊", 
    layout="centered"
)

# Custom High-End Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');

    /* Clean Body & Page Margin */
    .stApp {
        background-color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .main .block-container {
        padding-top: 3rem !important;
        max-width: 720px !important;
    }

    /* Headings */
    h1 {
        font-family: 'Playfair Display', serif !important;
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 2.2rem !important;
        line-height: 1.25 !important;
        margin-top: 0.5rem !important;
    }

    /* Subtitle & Body Text */
    p, span, label, [data-testid="stMarkdownContainer"] p {
        color: #1E293B !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 15px !important;
    }

    /* Cre8intech Demo Badge */
    .demo-badge {
        background-color: #0F172A !important;
        color: #F59E0B !important;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.2px;
        display: inline-block;
        margin-bottom: 8px;
        text-transform: uppercase;
    }

    /* Card Container */
    div[data-testid="stForm"] {
        background-color: #FFFDF5 !important;
        border: 2px solid #FCD34D !important;
        border-radius: 16px !important;
        padding: 28px !important;
        box-shadow: 0px 8px 24px rgba(245, 158, 11, 0.08) !important;
        margin-top: 15px !important;
    }

    /* Form Labels */
    label[data-testid="stWidgetLabel"] p {
        font-weight: 700 !important;
        color: #0F172A !important;
        font-size: 14.5px !important;
    }

    /* Money Wit Action Button */
    div.stButton > button,
    button[kind="primaryFormSubmit"],
    button[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%) !important;
        color: #0F172A !important;
        border-radius: 8px !important;
        border: 1px solid #D97706 !important;
        padding: 14px 28px !important;
        margin-top: 14px !important;
        box-shadow: 0px 4px 14px rgba(245, 158, 11, 0.35) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 14px !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        transition: all 0.2s ease-in-out !important;
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
st.markdown("**Configured for Money Wit Africa** (Founder: Oler Oladele, CFA)")
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
