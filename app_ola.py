import streamlit as st
import openai
import urllib.parse
from datetime import datetime

# Page Setup
st.set_page_config(
    page_title="Financial Diagnostic | Money Wit Africa", 
    page_icon="📊", 
    layout="centered"
)

# Custom Styling (Black Branded Dropdown + Gold Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');

    /* 1. Page Canvas & Spacing */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .main .block-container {
        padding-top: 3.5rem !important;
        max-width: 740px !important;
    }

    /* 2. Headings & Typography */
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

    /* Question Labels */
    label[data-testid="stWidgetLabel"] p {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 14.5px !important;
    }

    /* 3. Demo Badge */
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

    /* 4. Assessment Card */
    div[data-testid="stForm"], div.stBlock {
        background-color: #FFFDF5 !important;
        border: 2px solid #FCD34D !important;
        border-radius: 16px !important;
        padding: 28px !important;
        box-shadow: 0px 8px 24px rgba(245, 158, 11, 0.08) !important;
        margin-top: 15px !important;
        margin-bottom: 20px !important;
    }

    /* 5. Dropdown Styling */
    .stSelectbox div[data-baseweb="select"],
    .stSelectbox div[data-baseweb="select"] > div,
    .stSelectbox div[data-baseweb="select"] > div:first-child,
    .stSelectbox div[data-baseweb="select"] [role="combobox"],
    .stSelectbox div[data-baseweb="select"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #0F172A !important;
        background: #0F172A !important;
        border: 1.5px solid #F59E0B !important;
        border-radius: 8px !important;
        min-height: 46px !important;
    }

    .stSelectbox div[data-baseweb="select"] *,
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] div,
    .stSelectbox div[data-baseweb="select"] [role="combobox"] * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    .stSelectbox div[data-baseweb="select"] svg {
        fill: #F59E0B !important;
    }

    /* 6. Dropdown Options Menu */
    ul[role="listbox"] li,
    li[role="option"] {
        background-color: #FEF3C7 !important;
        border: 1px solid #FDE68A !important;
        border-radius: 6px !important;
        margin-bottom: 4px !important;
        color: #78350F !important;
        -webkit-text-fill-color: #78350F !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 10px 14px !important;
    }

    ul[role="listbox"] li:hover,
    li[role="option"]:hover,
    li[aria-selected="true"] {
        background-color: #FDE68A !important;
        color: #451A03 !important;
        -webkit-text-fill-color: #451A03 !important;
    }

    /* 7. Action Buttons */
    button[kind="primaryFormSubmit"],
    div[data-testid="stFormSubmitButton"] button,
    div.stButton > button {
        background-color: #F59E0B !important;
        background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%) !important;
        color: #0F172A !important;
        border-radius: 8px !important;
        border: 1px solid #D97706 !important;
        padding: 12px 24px !important;
        width: 100% !important;
        box-shadow: 0px 4px 14px rgba(245, 158, 11, 0.4) !important;
        transition: all 0.2s ease-in-out !important;
    }

    button[kind="primaryFormSubmit"] *,
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

    /* Custom Action Links (WhatsApp, Email & Products) */
    .dispatch-btn-wa {
        display: block;
        text-align: center;
        background-color: #25D366;
        color: #FFFFFF !important;
        font-weight: 800;
        padding: 12px 14px;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 4px;
        text-transform: uppercase;
        font-size: 13px;
        letter-spacing: 0.5px;
    }
    .dispatch-btn-wa:hover {
        background-color: #1EBE5D;
        color: #FFFFFF !important;
    }

    .dispatch-btn-email {
        display: block;
        text-align: center;
        background-color: #0F172A;
        color: #F59E0B !important;
        font-weight: 800;
        padding: 12px 14px;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 4px;
        text-transform: uppercase;
        font-size: 13px;
        letter-spacing: 0.5px;
        border: 1px solid #F59E0B;
    }
    .dispatch-btn-email:hover {
        background-color: #1E293B;
        color: #FBBF24 !important;
    }

    .product-card {
        background-color: #FFFDF5;
        border: 1.5px solid #FCD34D;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .product-btn {
        display: inline-block;
        background-color: #0F172A;
        color: #FFFFFF !important;
        font-size: 12.5px;
        font-weight: 700;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none;
        margin-top: 8px;
    }
    .product-btn:hover {
        background-color: #F59E0B;
        color: #0F172A !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<span class="demo-badge">CRE8INTECH PROTOTYPE DEMO</span>', unsafe_allow_html=True)
st.title("📊 Financial Health Diagnostic Tool")
st.caption("Configured for **Money Wit Africa** (Founder: Oler Oladele, CFA)")
st.write("Complete this 2-minute assessment to receive your personalized Wealth Archetype and custom Money Wit roadmap.")

# Assessment Form
with st.form("diagnostic_form"):
    st.subheader("1. Your Profile (Name is required)")
    user_name = st.text_input("Full Name *", placeholder="e.g. Amaka Adebayo")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        user_phone = st.text_input("WhatsApp Number (Optional)", placeholder="e.g. +234 801 234 5678")
    with col_c2:
        user_email = st.text_input("Email Address (Optional)", placeholder="e.g. amaka@example.com")
    
    st.subheader("2. Financial Health Assessment")
    earner_type = st.selectbox(
        "What best describes your current earning stage?",
        [
            "Early Career Professional", 
            "Mid-Level / Senior Professional", 
            "Business Owner / Entrepreneur", 
            "High-Net-Worth Individual"
        ]
    )
    
    primary_goal = st.selectbox(
        "What is your primary financial focus right now?",
        [
            "Building consistent monthly savings & emergency buffer", 
            "Investing in Eurobonds, FGN Sukuk & global equities", 
            "Clearing high-interest debt & cash flow optimization", 
            "Scaling and protecting a high-ticket wealth portfolio"
        ]
    )
    
    biggest_challenge = st.selectbox(
        "What is your biggest financial hurdle?",
        [
            "Financial jargon and investment complexity", 
            "Lack of time to analyze deals and market opportunities", 
            "Inconsistency in execution and accountability", 
            "Need for a vetted wealth circle and mastermind community"
        ]
    )
    
    submitted = st.form_submit_button("Generate My Wealth Roadmap 🚀")

# Process Diagnostic
if submitted:
    if not user_name.strip():
        st.error("Please provide your name before generating your roadmap.")
    else:
        api_key = st.secrets.get("OPENAI_API_KEY", "")
        if not api_key:
            st.error("Please configure your OPENAI_API_KEY in Streamlit Secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            
            prompt = f"""
            Analyze this user for Money Wit Africa (Founder: Oler Oladele, CFA):
            - Name: {user_name}
            - Earner Stage: {earner_type}
            - Primary Goal: {primary_goal}
            - Biggest Hurdle: {biggest_challenge}

            OUTPUT FORMAT:
            1. **Wealth Archetype:** (A sharp, empowering title, e.g., 'The Strategic Wealth Builder')
            2. **Financial Diagnostics:** (2 structured bullet points analyzing strengths and opportunities)
            3. **Your 3-Pillar Action Roadmap:** (3 tactical steps aligned directly with Money Wit resources):
               - Foundation/Habits -> The Money Wit School / Budgeting blueprints
               - Video Learning -> 'The Money Wit Show' on YouTube
               - Investing & Growth -> The Money Wit Club / Eurobond Masterclasses
            """
            
            with st.spinner("Diagnosing your wealth profile..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                summary = response.choices[0].message.content
                
            st.success(f"Assessment Complete for {user_name}!")
            st.markdown("---")
            st.markdown(summary)

            # Direct Website Product Match Cards
            st.markdown("---")
            st.subheader("🎯 Recommended Money Wit Pathways")
            st.write("Explore the exact programs and channels tailored to your diagnostic results:")

            prod_col1, prod_col2 = st.columns(2)
            with prod_col1:
                st.markdown("""
                <div class="product-card">
                    <h4>🏛️ The Money Wit Club</h4>
                    <p style="font-size: 13.5px;">For professionals & entrepreneurs ready to access Eurobonds, global investments, and curated deal rooms.</p>
                    <a href="https://themoneywit.africa/community/" target="_blank" class="product-btn">Explore The Club →</a>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="product-card">
                    <h4>🎓 The Money Wit School</h4>
                    <p style="font-size: 13.5px;">Master cashflow management, eliminate financial confusion, and build lifelong wealth habits.</p>
                    <a href="https://themoneywit.africa/" target="_blank" class="product-btn">Explore Courses →</a>
                </div>
                """, unsafe_allow_html=True)

            with prod_col2:
                st.markdown("""
                <div class="product-card">
                    <h4>📺 The Money Wit Show (YouTube)</h4>
                    <p style="font-size: 13.5px;">Watch in-depth weekly market breakdowns, investment strategies, and financial masterclasses.</p>
                    <a href="https://www.youtube.com/@themoneywitclub" target="_blank" class="product-btn">Watch on YouTube →</a>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="product-card">
                    <h4>⚡ Masterclasses & Bootcamps</h4>
                    <p style="font-size: 13.5px;">Short-term, intensive wealth acceleration bootcamps to fast-track your investment goals.</p>
                    <a href="https://themoneywit.africa/" target="_blank" class="product-btn">View Upcoming Sessions →</a>
                </div>
                """, unsafe_allow_html=True)

            # Module 3: Instant Dispatch Options (WhatsApp & Email)
            st.markdown("---")
            st.subheader("📤 Send & Save Your Roadmap")
            st.write("Share this diagnostic summary to your WhatsApp or Email for easy reference:")
            
            full_roadmap_text = (
                f"📊 *MONEY WIT AFRICA — WEALTH ROADMAP*\n"
                f"👤 *Client:* {user_name}\n"
                f"📅 *Date:* {datetime.now().strftime('%d %b %Y')}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{summary}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"✨ Next Steps: Explore programs at https://themoneywit.africa\n"
                f"📺 Watch 'The Money Wit Show' on YouTube: https://www.youtube.com/@themoneywitclub"
            )
            
            # WhatsApp Link
            encoded_wa = urllib.parse.quote(full_roadmap_text)
            wa_share_url = f"https://api.whatsapp.com/send?text={encoded_wa}"
            
            # Email Mailto Link
            email_subject = urllib.parse.quote(f"My Money Wit Wealth Roadmap - {user_name}")
            email_body = urllib.parse.quote(full_roadmap_text)
            target_email = user_email if user_email.strip() else ""
            mailto_url = f"mailto:{target_email}?subject={email_subject}&body={email_body}"

            col_send1, col_send2 = st.columns(2)
            with col_send1:
                st.markdown(f'<a href="{wa_share_url}" target="_blank" class="dispatch-btn-wa">📲 Send / Share via WhatsApp</a>', unsafe_allow_html=True)
            with col_send2:
                st.markdown(f'<a href="{mailto_url}" target="_blank" class="dispatch-btn-email">✉️ Send via Email</a>', unsafe_allow_html=True)
