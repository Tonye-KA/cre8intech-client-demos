import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Financial Diagnostic | Money Wit Africa", 
    page_icon="📊", 
    layout="centered"
)

# Header
st.markdown("### 📊 Financial Health Diagnostic Tool")
st.caption("Configured for **Money Wit Africa** (Founder: Oler Oladele, CFA)")
st.markdown("---")

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
    
    submitted = st.form_submit_button("Generate Financial Profile 🚀", type="primary")

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
