import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="CFG Wealth & Investment Navigator | CFG Africa", 
    page_icon="🏛️", 
    layout="centered"
)

# Custom Institutional Financial Styling (CFG Africa Brand)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');

    /* 1. Canvas & Layout */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .main .block-container {
        padding-top: 2.5rem !important;
        max-width: 780px !important;
    }

    /* 2. Typography */
    h1, h2, h3, h4 {
        font-family: 'Playfair Display', serif !important;
        color: #0B132B !important;
        font-weight: 700 !important;
        line-height: 1.25 !important;
    }

    p, span, label, [data-testid="stMarkdownContainer"] p, [data-testid="stCaptionContainer"] p {
        color: #1E293B !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    label[data-testid="stWidgetLabel"] p {
        color: #0B132B !important;
        font-weight: 700 !important;
        font-size: 14.5px !important;
    }

    /* 3. Cre8intech Demo Badge */
    .demo-badge {
        background-color: #0B132B !important;
        color: #14B8A6 !important; /* CFG Teal */
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.2px;
        display: inline-block;
        margin-bottom: 12px;
        text-transform: uppercase;
        box-shadow: 0px 2px 8px rgba(11, 19, 43, 0.15);
    }

    /* 4. Form Container Card */
    div[data-testid="stForm"], div.stBlock {
        background-color: #F8FAFC !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 14px !important;
        padding: 28px !important;
        box-shadow: 0px 8px 24px rgba(15, 23, 42, 0.06) !important;
        margin-top: 15px !important;
        margin-bottom: 20px !important;
    }

    /* 5. Dropdown Styling */
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] * {
        color: #0B132B !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="popover"],
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }

    ul[role="listbox"] li {
        color: #0B132B !important;
        font-weight: 600 !important;
    }

    ul[role="listbox"] li:hover {
        background-color: #F0FDFA !important;
        color: #0F766E !important;
    }

    /* 6. Signature CFG Teal Action Button */
    button[kind="primaryFormSubmit"],
    button[data-testid="baseButton-primary"],
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #0F766E 0%, #0B132B 100%) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 14px 28px !important;
        width: 100% !important;
        margin-top: 14px !important;
        box-shadow: 0px 4px 14px rgba(15, 118, 110, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }

    button[kind="primaryFormSubmit"] *,
    div[data-testid="stFormSubmitButton"] button * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 14px !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }

    button[kind="primaryFormSubmit"]:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0px 6px 18px rgba(15, 118, 110, 0.45) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<span class="demo-badge">CRE8INTECH PROTOTYPE DEMO</span>', unsafe_allow_html=True)
st.title("🏛️ CFG Wealth & Investment Navigator")
st.caption("Configured for **CFG Africa** (Managing Director: Babajide Lawani)")
st.write("Discover which CFG investment product, multi-currency placement, ethical fund, or wealth advisory solution matches your financial goals.")

# System Prompt incorporating all CFG Consumer Offerings
SYSTEM_PROMPT = """
You are the CFG Wealth & Investment Concierge for CFG Africa (Managing Director: Babajide Lawani).
Your role is to analyze the user's financial profile and route them to the exact product(s) in CFG Africa's ecosystem.

CFG AFRICA'S CONSUMER PRODUCT ECOSYSTEM:
1. CFG AM Naira Fixed Income Fund (SEC-regulated mutual fund for steady, inflation-hedging yield and daily unit liquidity).
2. Multi-Currency Tenured Placements (FX capital preservation & fixed yields in USD, GBP, EUR, and NGN).
3. Non-Interest / Halal Permissible Investments (Sharia-compliant, Ijarah-based ethical models, Riba-free capital growth).
4. Fixed Rate Notes & Depository Notes (Predetermined SEC-regulated fixed returns shielding capital from volatility).
5. Government Securities & Treasury Bills (Direct access to primary & secondary sovereign markets).
6. CFG Private Wealth, Family Office & Estate Planning / Trusts (Generational wealth transfer, tax advisory, discretionary portfolios for HNWIs).

OUTPUT FORMAT:
1. **Investor Persona Summary:** (1-2 sharp lines summarizing their strategy profile)
2. **Primary Recommended CFG Product:** (Exact name of the CFG product and why it fits)
3. **Complementary Diversification Product:** (A secondary CFG instrument to balance risk or currency exposure)
4. **Estimated Allocation Blueprint:** (Suggested % split across instruments)
5. **Next Steps to Subscribe:** (Clear call to action to onboard with CFG Asset Management / Wealth desk)
"""

# Dynamic Multi-Product Form
with st.form("cfg_navigator_form"):
    user_type = st.selectbox(
        "1. What best describes your investor profile?",
        [
            "Working Professional / Salary Earner (Seeking inflation protection & steady growth)",
            "Diaspora / Remote Earner (Managing multi-currency income in USD / GBP / EUR)",
            "Faith-Conscious / Ethical Investor (Requiring strict Sharia / Halal compliance)",
            "Business Owner / High-Net-Worth Individual (Focusing on capital preservation & succession)",
            "Retiree / Conservative Saver (Prioritizing guaranteed fixed income and capital safety)"
        ]
    )

    core_goal = st.selectbox(
        "2. What is your primary investment objective?",
        [
            "Stable monthly/quarterly passive income (Shielded from market volatility)",
            "Foreign currency hedge & wealth preservation (USD / GBP placements)",
            "Ethical & interest-free (Riba-free) capital appreciation",
            "Long-term generational wealth transfer & private trust setup",
            "Liquid emergency/short-term treasury reserve (90 - 180 days)"
        ]
    )

    capital_horizon = st.selectbox(
        "3. What is your preferred investment horizon & risk tolerance?",
        [
            "Short-Term Liquidity (30 - 90 Days) with Low Risk",
            "Medium-Term Growth (6 - 12 Months) with Moderate Risk",
            "Long-Term Multi-Year Compounding (1 - 5 Years) with Capital Preservation",
            "Generational / Structured Estate (Multi-Year Trust Mandate)"
        ]
    )

    submitted = st.form_submit_button("Generate Custom CFG Investment Plan 🚀")

if submitted:
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        st.error("Please configure OPENAI_API_KEY in Streamlit Secrets.")
    else:
        client = openai.OpenAI(api_key=api_key)
        prompt = f"""
        User Profile: {user_type}
        Investment Objective: {core_goal}
        Horizon & Risk: {capital_horizon}
        
        Generate a personalized CFG Africa investment recommendation and allocation mandate following the system guidelines.
        """
        
        with st.spinner("CFG Navigator is structuring your investment recommendation..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content

        st.success("Your CFG Investment Match is Ready!")
        st.markdown("---")
        st.markdown(result)
