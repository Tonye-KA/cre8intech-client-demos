import streamlit as st
import openai
import urllib.parse
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="CFG Enterprise Wealth Suite | CFG Africa",
    page_icon="🏛️",
    layout="wide"
)

# Custom Corporate CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #080D1A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #F1F5F9 !important;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .main .block-container {
        padding-top: 1.8rem !important;
        max-width: 1100px !important;
    }

    h1, h2, h3, h4 {
        font-family: 'Playfair Display', serif !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    p, span, label, [data-testid="stMarkdownContainer"] p {
        color: #CBD5E1 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    label[data-testid="stWidgetLabel"] p {
        color: #38BDF8 !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    .suite-badge {
        background-color: #1E293B !important;
        color: #14B8A6 !important;
        border: 1px solid #0F766E;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.2px;
        display: inline-block;
        margin-bottom: 12px;
        text-transform: uppercase;
    }

    /* Tabs Styling */
    div[data-baseweb="tab-list"] {
        background-color: #0F172A !important;
        border-radius: 10px !important;
        padding: 6px !important;
        border: 1px solid #1E293B !important;
    }

    button[data-baseweb="tab"] {
        border-radius: 6px !important;
        padding: 10px 20px !important;
    }

    button[data-baseweb="tab"] p {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
    }

    button[aria-selected="true"] {
        background-color: #1E293B !important;
    }

    button[aria-selected="true"] p {
        color: #38BDF8 !important;
    }

    /* Form Container */
    div[data-testid="stForm"] {
        background-color: #0F172A !important;
        border: 1px solid #1E293B !important;
        border-radius: 12px !important;
        padding: 24px !important;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5) !important;
    }

    /* Inputs */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] > div {
        background-color: #080D1A !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
    }

    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
    }

    /* Action Buttons */
    button[kind="primaryFormSubmit"],
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #0F766E 0%, #0284C7 100%) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 14px 28px !important;
        width: 100% !important;
        margin-top: 10px !important;
        font-size: 14px !important;
        font-weight: 800 !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        box-shadow: 0px 4px 16px rgba(15, 118, 110, 0.4) !important;
    }

    .action-btn-whatsapp {
        display: inline-block;
        background-color: #25D366;
        color: #FFFFFF !important;
        font-weight: 700;
        padding: 12px 20px;
        border-radius: 8px;
        text-decoration: none;
        text-align: center;
        width: 100%;
        box-sizing: border-box;
    }

    .action-btn-email {
        display: inline-block;
        background-color: #0284C7;
        color: #FFFFFF !important;
        font-weight: 700;
        padding: 12px 20px;
        border-radius: 8px;
        text-decoration: none;
        text-align: center;
        width: 100%;
        box-sizing: border-box;
    }

    .output-box {
        background-color: #0F172A;
        border-radius: 10px;
        padding: 22px;
        margin-top: 12px;
        margin-bottom: 20px;
    }

    .box-memo { border: 1.5px solid #38BDF8; }
    </style>
""", unsafe_allow_html=True)

# Shared Log State
if "activity_logs" not in st.session_state:
    st.session_state["activity_logs"] = [
        {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Module": "Module 1: Mandate Structuring",
            "Client / Mandate": "Tier-1 Corporate Treasury",
            "Capital Volume": "₦150,000,000 + $75,000 USD",
            "Action Status": "Mandate Strategy Calculated & Filed"
        },
        {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Module": "Module 2: Negotiation Desk",
            "Client / Mandate": "Alhaji Garba (Crestline Ventures)",
            "Capital Volume": "CFG AM Naira Fixed Income Fund",
            "Action Status": "Objection Handled & WhatsApp Briefing Dispatched"
        }
    ]

# Header
st.markdown('<span class="suite-badge">CRE8INTECH ENTERPRISE SUITE</span>', unsafe_allow_html=True)
st.title("🏛️ CFG Unified RM Wealth & Deal Suite")
st.caption("Institutional Portfolio Structuring, Objection Resolution & Sales Enablement")

api_key = st.secrets.get("OPENAI_API_KEY", "")

tab1, tab2 = st.tabs([
    "📊 Module 1: Institutional RM Mandate Diagnostician", 
    "🥊 Module 2: RM Negotiate & Battle Desk"
])

# ==============================================================================
# MODULE 1: MANDATE DIAGNOSTICIAN
# ==============================================================================
with tab1:
    st.subheader("Institutional Portfolio Diagnostician & Mandate Builder")
    st.write("Advanced structuring tool for Wealth Advisors during corporate and HNWI mandate onboarding.")

    with st.form("rm_diagnostician_form"):
        col1, col2 = st.columns(2)
        with col1:
            client_profile = st.selectbox(
                "Client Mandate Classification:",
                [
                    "Tier-1 Corporate Treasury (Working Capital / Tax Reserve)",
                    "Ultra-High-Net-Worth Family Office (Generational Trust & Succession)",
                    "Diaspora Executive / Foreign Earner (Multi-Currency Accumulator)",
                    "Faith-Conscious Institutional Mandate (Strict Non-Interest / Riba-Free)",
                    "Mid-Market Enterprise (Surplus Liquidity Management)"
                ]
            )
            naira_capital = st.text_input("Naira Capital Volume (NGN):", value="₦150,000,000")
            fx_capital = st.text_input("Foreign Currency Volume (USD / GBP / EUR):", value="$75,000 USD")

        with col2:
            staggered_liquidity = st.selectbox(
                "Liquidity Drawdown & Maturity Constraints:",
                [
                    "High Liquidity (30-day rolling access required for operational cashflow)",
                    "Staggered Tranches (30% at 90 days, 70% at 364 days)",
                    "Locked Fixed Tenor (12 to 24 Months Capital Compounding)",
                    "Perpetual Multi-Year Trust Structure (Quarterly Coupon Distribution)"
                ]
            )
            tax_objective = st.selectbox(
                "Tax & Yield Optimization Priority:",
                [
                    "Maximize After-Tax Yield (Utilize SEC WHT-exempt mutual fund structures)",
                    "Capital Preservation & Currency Hedge over Maximum Nominal Yield",
                    "Asset-Backed Tangible Financing (Ijarah / Sukuk Profit Distribution)",
                    "Blended High-Yield Fixed Income + Commercial Paper Spread"
                ]
            )

        advisor_notes = st.text_area("Specific RM Advisory Notes / Benchmark Mandates:", placeholder="e.g. Client benchmarked against Stanbic IBTC Money Market and wants higher USD yields...", height=70)
        submit_diag = st.form_submit_button("Calculate Institutional Strategy 📊")

    if submit_diag:
        if not api_key:
            st.error("Please add OPENAI_API_KEY to Streamlit Secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt_diag = f"""
            You are the Chief Investment Structuring Officer at CFG Africa assisting an RM.
            Managing Director: Babajide Lawani.

            INPUTS:
            - Client Class: {client_profile}
            - Capital: {naira_capital} + {fx_capital}
            - Liquidity: {staggered_liquidity}
            - Tax/Yield Target: {tax_objective}
            - RM Notes: {advisor_notes}

            DELIVER A BOARDROOM-READY MANDATE REPORT:
            1. 💼 Executive Mandate Strategy: 2-line strategic thesis.
            2. 🏛️ Structured Portfolio Allocation Breakdown across CFG Funds, FX Placements, CPs, and Halal Sukuk.
            3. 📈 Yield & WHT Optimization Rationale.
            4. 📋 Investment Committee Internal Tear-Sheet.
            """
            with st.spinner("Calculating Mandate Structure..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_diag}]
                )
                st.session_state["diag_output"] = res.choices[0].message.content
                st.session_state["diag_calculated"] = True
                st.session_state["current_mandate_class"] = client_profile
                st.session_state["current_mandate_cap"] = f"{naira_capital} + {fx_capital}"

    if st.session_state.get("diag_calculated"):
        st.markdown("### 📋 Structured Portfolio Mandate & Tear-Sheet")
        st.markdown('<div class="output-box box-memo">', unsafe_allow_html=True)
        st.markdown(st.session_state["diag_output"])
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Log Mandate to Management Deal Tracker ✅"):
            st.session_state["activity_logs"].insert(0, {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Module": "Module 1: Mandate Structuring",
                "Client / Mandate": st.session_state.get("current_mandate_class", "Institutional Client"),
                "Capital Volume": st.session_state.get("current_mandate_cap", "₦150M"),
                "Action Status": "Mandate Strategy Logged to Central Pipeline"
            })
            st.success(" Mandate Successfully Logged to CFG Activity Log.")

# ==============================================================================
# MODULE 2: NEGOTIATE & BATTLE DESK
# ==============================================================================
with tab2:
    st.subheader("Live Deal-Closer & Sales Enablement Desk")
    st.write("Overcome objections live, structure deal packages, and unlock instant client dispatch channels.")

    with st.form("rm_battle_form"):
        col1, col2 = st.columns(2)
        with col1:
            target_entity = st.text_input("Prospect / Corporate Name:", value="Alhaji Garba (Crestline Ventures)")
            active_product = st.selectbox(
                "Product Under Negotiation:",
                [
                    "CFG AM Naira Fixed Income Fund (SEC Regulated)",
                    "CFG Multi-Currency Tenured Placement (USD/GBP)",
                    "Corporate Commercial Paper (CP) High-Yield Note",
                    "Non-Interest / Halal Sukuk & Ijarah Portfolio",
                    "CFG Private Trust & Family Office Structure"
                ]
            )
        with col2:
            objection_type = st.selectbox(
                "Client Objection / Competitor Pushback:",
                [
                    "Objection: 'Why choose CFG Mutual Fund over buying Treasury Bills directly on banking apps?'",
                    "Objection: 'Why place foreign currency with CFG instead of leaving it in a Domiciliary Account?'",
                    "Objection: 'Your corporate commercial paper yield is high, but how safe is my principal?'",
                    "Objection: 'How do you guarantee this product is 100% Sharia / Halal compliant?'",
                    "Custom Objection / Price Pushback"
                ]
            )
            deal_context = st.text_input("Context (e.g. Competitor mentioned):", value="Client is comparing with a commercial bank fixed deposit offering 17%")

        submit_battle = st.form_submit_button("Generate Battle Desk & Deal Package ⚡")

    if submit_battle:
        if not api_key:
            st.error("Please add OPENAI_API_KEY to Streamlit Secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            
            prompt_battle_card = f"""
            You are the Senior Sales Enablement Officer at CFG Africa (MD: Babajide Lawani).
            Generate the Battle Resolution Desk response for:
            Client: {target_entity} | Product: {active_product} | Objection: {objection_type} | Context: {deal_context}

            OUTPUT FORMAT:
            1. 🥊 **Objection Resolution & Strategic Angles:** Exactly 3 sharp, compliance-aligned counter-arguments addressing the objection.
            2. 💼 **Internal Deal Summary:** 2-line strategic deal note.
            3. 🎯 **Recommended Next Action:** Clear, actionable next step for the RM.
            """

            prompt_whatsapp = f"""
            Draft an executive WhatsApp message from CFG Africa RM to:
            Client: {target_entity} | Product: {active_product} | Context: {deal_context}

            Keep it concise with professional bullet points, next steps, and sign-off:
            ───────────────────────────────
            🏛️ CFG Africa | Wealth Management & Advisory
            Regulated by the Securities & Exchange Commission (SEC)
            Website: https://cfgafrica.com
            ───────────────────────────────
            """

            prompt_email = f"""
            Draft a formal Boardroom-Ready Corporate Email Proposal from CFG Africa to:
            Client: {target_entity} | Product: {active_product} | Context: {deal_context}

            Include Subject line, executive greeting, strategic rationale, regulatory safeguards, and account onboarding instructions.
            """

            with st.spinner("Structuring Deal Strategy & Battle Desk Arguments..."):
                res1 = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_battle_card}]
                )
                res2 = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_whatsapp}]
                )
                res3 = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_email}]
                )

                st.session_state["target_entity"] = target_entity
                st.session_state["active_product"] = active_product
                st.session_state["battle_card"] = res1.choices[0].message.content
                st.session_state["whatsapp_text"] = res2.choices[0].message.content
                st.session_state["email_text"] = res3.choices[0].message.content
                st.session_state["battle_generated"] = True
                st.session_state["battle_logged"] = False

    if st.session_state.get("battle_generated"):
        st.markdown("### 🥊 1. Objection Battle Resolution & Mandate Note")
        st.markdown('<div class="output-box box-memo">', unsafe_allow_html=True)
        st.markdown(st.session_state["battle_card"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🔒 Step 2: Log Deal Review & Unlock Dispatch Channels")
        
        if not st.session_state.get("battle_logged"):
            if st.button("Log Deal Review & Unlock Dispatch Channels 📥"):
                st.session_state["battle_logged"] = True
                st.session_state["activity_logs"].insert(0, {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Module": "Module 2: Negotiation Desk",
                    "Client / Mandate": st.session_state.get("target_entity", "Client"),
                    "Capital Volume": st.session_state.get("active_product", "CFG Placement"),
                    "Action Status": "Objection Handled & Proposal Ready"
                })
                st.rerun()
        else:
            st.success(" Deal Logged to Activity Tracker. Instant Dispatch Channels Unlocked Below:")
            
            client_name_safe = st.session_state.get("target_entity", "Client")
            encoded_wa = urllib.parse.quote(st.session_state["whatsapp_text"])
            encoded_email_body = urllib.parse.quote(st.session_state["email_text"])
            encoded_subject = urllib.parse.quote(f"CFG Africa Investment Mandate Proposal - {client_name_safe}")

            btn_col1, btn_col2, btn_col3 = st.columns(3)

            with btn_col1:
                st.markdown(
                    f'<a href="https://wa.me/?text={encoded_wa}" target="_blank" class="action-btn-whatsapp">📲 Open in WhatsApp</a>', 
                    unsafe_allow_html=True
                )
                st.caption("Pre-populates executive WhatsApp briefing.")

            with btn_col2:
                st.markdown(
                    f'<a href="mailto:?subject={encoded_subject}&body={encoded_email_body}" class="action-btn-email">✉️ Open in Email App</a>', 
                    unsafe_allow_html=True
                )
                st.caption("Pre-populates corporate email proposal.")

            with btn_col3:
                st.download_button(
                    label="📄 Export Mandate Document",
                    data=st.session_state["email_text"],
                    file_name=f"CFG_Mandate_{client_name_safe.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.caption("Downloads text for official letterhead.")

# ==============================================================================
# UNIFIED ACTIVITY & MANAGEMENT LOG (BOTTOM EXPANDER)
# ==============================================================================
st.markdown("---")
with st.expander("📊 Executive Activity Log & Pipeline Telemetry (Management View)", expanded=False):
    st.write("Real-time logging of institutional mandates diagnosed and deal actions dispatched across the advisory desk.")
    if st.session_state["activity_logs"]:
        df_logs = pd.DataFrame(st.session_state["activity_logs"])
        st.dataframe(df_logs, use_container_width=True, hide_index=True)
    else:
        st.info("No activity logged yet.")
