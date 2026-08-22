import streamlit as st
import openai
import urllib.parse
import pandas as pd
from datetime import datetime, date, timedelta

# Page Configuration
st.set_page_config(
    page_title="CFG Enterprise Wealth & Deal Suite | CFG Africa",
    page_icon="🏛️",
    layout="wide"
)

# Custom Corporate CSS (CFG Executive Navy & Emerald Theme)
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
        padding-top: 1.5rem !important;
        max-width: 1200px !important;
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
        font-size: 12px !important;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    .suite-badge {
        background-color: #1E293B !important;
        color: #14B8A6 !important;
        border: 1px solid #0F766E;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.2px;
        display: inline-block;
        margin-bottom: 8px;
        text-transform: uppercase;
    }

    .demo-banner {
        background-color: #1E293B;
        border-left: 4px solid #F59E0B;
        padding: 8px 14px;
        border-radius: 4px;
        font-size: 12px;
        color: #FCD34D !important;
        margin-bottom: 15px;
    }

    .governance-notice {
        background-color: #0F172A;
        border: 1px solid #334155;
        border-left: 3px solid #38BDF8;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 12px;
        color: #94A3B8 !important;
        margin-top: 10px;
        margin-bottom: 12px;
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
        padding: 10px 18px !important;
    }

    button[data-baseweb="tab"] p {
        font-size: 13px !important;
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
        padding: 22px !important;
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
        padding: 12px 24px !important;
        width: 100% !important;
        margin-top: 8px !important;
        font-size: 13px !important;
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
        padding: 12px 18px;
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
        padding: 12px 18px;
        border-radius: 8px;
        text-decoration: none;
        text-align: center;
        width: 100%;
        box-sizing: border-box;
    }

    /* Output Card */
    .output-box {
        background-color: #0F172A;
        border-radius: 10px;
        padding: 20px;
        margin-top: 12px;
        margin-bottom: 18px;
    }

    .box-memo { border: 1.5px solid #38BDF8; }

    /* KPI Metrics Cards */
    .kpi-card {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 14px 18px;
        text-align: left;
    }
    .kpi-title {
        font-size: 11px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 20px;
        font-weight: 800;
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# Helper: Format Currency NGN
def fmt_ngn(val):
    return f"₦{val:,.0f}"

# Helper: Calculate Deal Health
def get_deal_health(due_date_val, stage):
    if stage == "Won":
        return "🟢 Healthy"
    if stage == "Lost":
        return "⚪ Closed"
    
    today = date.today()
    if isinstance(due_date_val, str):
        try:
            due_date_val = datetime.strptime(due_date_val, "%Y-%m-%d").date()
        except:
            return "🟢 Healthy"
            
    if due_date_val > today:
        return "🟢 Healthy"
    elif due_date_val == today:
        return "🟡 At Risk"
    else:
        return "🔴 Stalled"

# Initialize Demo Pipeline Data in Session State
if "deals_db" not in st.session_state:
    st.session_state["deals_db"] = [
        {
            "id": "DEAL-001",
            "client_name": "Alhaji Garba",
            "company": "Crestline Ventures",
            "rm_name": "Tunde Bakare (RM)",
            "product": "CFG AM Naira Fixed Income Fund",
            "value": 150000000,
            "stage": "Negotiation",
            "prob": 75,
            "close_date": str(date.today() + timedelta(days=5)),
            "next_action": "Present after-tax WHT comparison memo to Investment Committee",
            "due_date": str(date.today() + timedelta(days=2)),
            "date_logged": str(date.today() - timedelta(days=4)),
            "history": [
                f"{str(date.today() - timedelta(days=4))} 09:15 — Mandate Diagnosed (₦150M)",
                f"{str(date.today() - timedelta(days=2))} 14:30 — Objection Battle Card Generated & Briefing Dispatched",
                f"{str(date.today() - timedelta(days=1))} 11:00 — Deal Stage Updated to Negotiation"
            ]
        },
        {
            "id": "DEAL-002",
            "client_name": "Dr. Florence Adeleke",
            "company": "MedEquip International",
            "rm_name": "Tunde Bakare (RM)",
            "product": "CFG Multi-Currency Tenured Placement (USD)",
            "value": 115000000, # ~$75k USD equiv
            "stage": "Proposal Sent",
            "prob": 60,
            "close_date": str(date.today() + timedelta(days=10)),
            "next_action": "Follow up via executive WhatsApp briefing on USD coupon timing",
            "due_date": str(date.today()), # Due today -> At Risk
            "date_logged": str(date.today() - timedelta(days=2)),
            "history": [
                f"{str(date.today() - timedelta(days=2))} 16:45 — USD Placement Mandate Diagnosed",
                f"{str(date.today() - timedelta(days=2))} 17:00 — Boardroom Proposal Sent via Email"
            ]
        },
        {
            "id": "DEAL-003",
            "client_name": "Chief Emeka Nnaji",
            "company": "Nnaji Transport Logistics",
            "rm_name": "Ngozi Eze (Senior RM)",
            "product": "Corporate Commercial Paper (CP) High-Yield Note",
            "value": 250000000,
            "stage": "Qualified",
            "prob": 40,
            "close_date": str(date.today() + timedelta(days=20)),
            "next_action": "Obtain audited H1 financials for CP credit rating memo",
            "due_date": str(date.today() - timedelta(days=2)), # Overdue -> Stalled
            "date_logged": str(date.today() - timedelta(days=8)),
            "history": [
                f"{str(date.today() - timedelta(days=8))} 10:20 — Initial Corporate Treasury Request",
                f"{str(date.today() - timedelta(days=5))} 12:10 — Credit Guarantee Battle Card Reviewed"
            ]
        },
        {
            "id": "DEAL-004",
            "client_name": "Tariq Halal Foundation",
            "company": "Tariq Global Waqf",
            "rm_name": "Ngozi Eze (Senior RM)",
            "product": "Non-Interest / Halal Sukuk & Ijarah Portfolio",
            "value": 300000000,
            "stage": "Won",
            "prob": 100,
            "close_date": str(date.today() - timedelta(days=1)),
            "next_action": "Execute Sukuk tranche allocation & mandate agreement",
            "due_date": str(date.today() + timedelta(days=15)),
            "date_logged": str(date.today() - timedelta(days=14)),
            "history": [
                f"{str(date.today() - timedelta(days=14))} 11:30 — Non-Interest Mandate Diagnosed",
                f"{str(date.today() - timedelta(days=7))} 15:00 — Sharia Advisory Verification Sent",
                f"{str(date.today() - timedelta(days=1))} 16:30 — Mandate Won & Funds Inflow Received"
            ]
        },
        {
            "id": "DEAL-005",
            "client_name": "Mrs. Funke Balogun",
            "company": "Balogun Family Trust",
            "rm_name": "Femi Adele (RM)",
            "product": "CFG Private Trust & Family Office Structure",
            "value": 200000000,
            "stage": "New",
            "prob": 20,
            "close_date": str(date.today() + timedelta(days=30)),
            "next_action": "Schedule introductory trust structuring discovery session",
            "due_date": str(date.today() + timedelta(days=3)),
            "date_logged": str(date.today()),
            "history": [
                f"{str(date.today())} 08:45 — Inbound Advisory Referral Logged"
            ]
        }
    ]

# Header & Role Access Selector
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown('<span class="suite-badge">CRE8INTECH ENTERPRISE SUITE</span>', unsafe_allow_html=True)
    st.title("🏛️ CFG Unified RM Wealth & Deal Suite")
    st.caption("AI Mandate Structuring, Live Objection Battle Cards & Management Deal Pipeline")
with header_col2:
    st.markdown("**Enterprise Role Perspective:**")
    role = st.selectbox(
        "Select User Role:",
        ["RM User (Tunde Bakare)", "Executive Management (MD / Head of Wealth)"],
        label_visibility="collapsed"
    )

st.markdown("""
<div class="demo-banner">
    ⚠️ <strong>DEMO DATA & ACCESS CONTROL:</strong> Fictional client and mandate data for executive demonstration. Production deployment integrates with CFG single sign-on (SSO) and role-based access.
</div>
""", unsafe_allow_html=True)

api_key = st.secrets.get("OPENAI_API_KEY", "")

# Top-Level Navigation Tabs
if role.startswith("RM User"):
    main_tab1, main_tab2 = st.tabs(["🏛️ RM Deal Desk", "📊 Deal Pipeline (My Deals)"])
    has_mgmt = False
else:
    main_tab1, main_tab2, main_tab3 = st.tabs(["🏛️ RM Deal Desk", "📊 Deal Pipeline (All Deals)", "📈 Executive Management Dashboard"])
    has_mgmt = True

# ==============================================================================
# SECTION 1: RM DEAL DESK (PRESERVED & ENHANCED)
# ==============================================================================
with main_tab1:
    sub_tab1, sub_tab2 = st.tabs([
        "📊 Module 1: Institutional RM Mandate Diagnostician", 
        "🥊 Module 2: RM Negotiate & Battle Card Desk"
    ])

    # Module 1: Diagnostician
    with sub_tab1:
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
                with st.spinner("Calculating Mandate..."):
                    res = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt_diag}]
                    )
                    st.session_state["diag_output"] = res.choices[0].message.content
                    st.session_state["diag_calculated"] = True

        if st.session_state.get("diag_calculated"):
            st.markdown("### 📋 Structured Portfolio Mandate & Tear-Sheet")
            st.markdown('<div class="output-box box-memo">', unsafe_allow_html=True)
            st.markdown(st.session_state["diag_output"])
            st.markdown('</div>', unsafe_allow_html=True)

    # Module 2: Battle Card & Deal Closer
    with sub_tab2:
        st.subheader("Live Deal-Closer & Sales Enablement Desk")
        st.write("Overcome objections live, structure deal packages, and log opportunities directly to the pipeline.")

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

            submit_battle = st.form_submit_button("Generate Battle Card & Deal Package ⚡")

        if submit_battle:
            if not api_key:
                st.error("Please add OPENAI_API_KEY to Streamlit Secrets.")
            else:
                client = openai.OpenAI(api_key=api_key)
                
                prompt_battle_card = f"""
                You are the Senior Sales Enablement Copilot at CFG Africa (MD: Babajide Lawani).
                Client: {target_entity} | Product: {active_product} | Objection: {objection_type} | Context: {deal_context}

                OUTPUT FORMAT:
                1. 🥊 **RM Objection Counter-Arguments:** Exactly 3 sharp, compliance-aligned counter-arguments addressing this objection.
                2. 💼 **Internal Deal Summary:** 2-line strategic deal note.
                3. 🎯 **Recommended Next Action:** A practical, time-bound next step for the RM (e.g. 'Follow up within 24 hours with the executive proposal and address the client\\'s liquidity concern.').
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

                with st.spinner("Structuring Deal Strategy & AI Battle Card..."):
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
                    st.session_state["deal_logged_current"] = False

        if st.session_state.get("battle_generated"):
            st.markdown("### 🥊 1. RM Objection Battle Card & Internal Memo")
            st.markdown('<div class="output-box box-memo">', unsafe_allow_html=True)
            st.markdown(st.session_state["battle_card"])
            st.markdown('</div>', unsafe_allow_html=True)

            # Governance Notice
            st.markdown("""
            <div class="governance-notice">
                🛡️ <strong>AI-Assisted Output:</strong> Review and verify details before logging to pipeline or dispatching client communications.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 🔒 Step 2: Log Opportunity to Deal Pipeline")

            # Capture Deal Value & Parameters for Pipeline
            with st.form("log_deal_to_pipeline_form"):
                col_p1, col_p2, col_p3 = st.columns(3)
                with col_p1:
                    log_mandate_val = st.number_input("Estimated Mandate Value (NGN):", value=150000000, step=5000000)
                    log_stage = st.selectbox("Deal Stage:", ["New", "Qualified", "Proposal Sent", "Negotiation", "Won", "Lost"], index=3)
                with col_p2:
                    log_prob = st.slider("Closing Probability (%):", 0, 100, 75, step=5)
                    log_close_date = st.date_input("Expected Close Date:", value=date.today() + timedelta(days=14))
                with col_p3:
                    log_next_action = st.text_input("Next Action:", value="Follow up on WHT comparison and proposal draft")
                    log_due_date = st.date_input("Next Action Due Date:", value=date.today() + timedelta(days=2))

                submit_log_deal = st.form_submit_button("Confirm & Log Deal to Pipeline 📥")

            if submit_log_deal:
                # Add to in-memory deals database
                new_deal_entry = {
                    "id": f"DEAL-00{len(st.session_state['deals_db']) + 1}",
                    "client_name": st.session_state.get("target_entity", "Valued Client").split("(")[0].strip(),
                    "company": st.session_state.get("target_entity", "Corporate").split("(")[1].replace(")", "") if "(" in st.session_state.get("target_entity", "") else "Private Enterprise",
                    "rm_name": "Tunde Bakare (RM)",
                    "product": st.session_state.get("active_product", "CFG AM Fixed Income"),
                    "value": float(log_mandate_val),
                    "stage": log_stage,
                    "prob": int(log_prob),
                    "close_date": str(log_close_date),
                    "next_action": log_next_action,
                    "due_date": str(log_due_date),
                    "date_logged": str(date.today()),
                    "history": [
                        f"{str(date.today())} {datetime.now().strftime('%H:%M')} — Battle Card Generated & Opportunity Logged (Stage: {log_stage})"
                    ]
                }
                st.session_state["deals_db"].insert(0, new_deal_entry)
                st.session_state["deal_logged_current"] = True
                st.success(" Opportunity Successfully Logged to Deal Pipeline & Management Tracker.")

            if st.session_state.get("deal_logged_current"):
                st.markdown("### 🚀 Instant Client Dispatch Channels (Unlocked)")
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
# SECTION 2: DEAL PIPELINE TAB
# ==============================================================================
with main_tab2:
    st.subheader("CFG Wealth Advisory Deal Pipeline")
    st.write("Live repository of all institutional opportunities logged across the advisory team.")

    # Filter by user role / ownership
    deals_data = list(st.session_state["deals_db"])
    
    if role.startswith("RM User"):
        view_mode = st.radio("Pipeline View:", ["My Deals", "All Deals"], horizontal=True, index=0)
    else:
        view_mode = st.radio("Pipeline View:", ["My Deals", "All Deals"], horizontal=True, index=1)

    if view_mode == "My Deals":
        deals_data = [d for d in deals_data if "Tunde Bakare" in d["rm_name"]]

    # Search and Multi-Filter Bar
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with f_col1:
        search_query = st.text_input("🔍 Search Client / Company:", placeholder="e.g. Garba, Crestline...")
    with f_col2:
        stage_filter = st.multiselect("Filter by Stage:", ["New", "Qualified", "Proposal Sent", "Negotiation", "Won", "Lost"])
    with f_col3:
        product_filter = st.multiselect("Filter by Product:", list(set([d["product"] for d in deals_data])))
    with f_col4:
        health_filter = st.multiselect("Filter by Health:", ["🟢 Healthy", "🟡 At Risk", "🔴 Stalled", "⚪ Closed"])

    # Apply Filters
    filtered_deals = []
    for d in deals_data:
        d_health = get_deal_health(d["due_date"], d["stage"])
        if search_query:
            q = search_query.lower()
            if q not in d["client_name"].lower() and q not in d["company"].lower():
                continue
        if stage_filter and d["stage"] not in stage_filter:
            continue
        if product_filter and d["product"] not in product_filter:
            continue
        if health_filter and d_health not in health_filter:
            continue
        filtered_deals.append(d)

    # Top KPI Metrics Cards
    active_deals = [d for d in filtered_deals if d["stage"] not in ["Won", "Lost"]]
    won_deals = [d for d in filtered_deals if d["stage"] == "Won"]
    
    total_pipeline_val = sum([d["value"] for d in active_deals])
    weighted_pipeline_val = sum([d["value"] * (d["prob"] / 100.0) for d in active_deals])
    won_mandate_val = sum([d["value"] for d in won_deals])
    proposals_count = len([d for d in filtered_deals if d["stage"] in ["Proposal Sent", "Negotiation", "Won"]])

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Active Deals</div><div class="kpi-value">{len(active_deals)}</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Pipeline</div><div class="kpi-value">{fmt_ngn(total_pipeline_val)}</div></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Weighted Value</div><div class="kpi-value">{fmt_ngn(weighted_pipeline_val)}</div></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Proposals Sent</div><div class="kpi-value">{proposals_count}</div></div>', unsafe_allow_html=True)
    with kpi5:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Won Mandates</div><div class="kpi-value">{fmt_ngn(won_mandate_val)}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Table Display of Logged Deals
    if filtered_deals:
        table_rows = []
        for d in filtered_deals:
            table_rows.append({
                "Deal ID": d["id"],
                "Client & Company": f"{d['client_name']} ({d['company']})",
                "RM Owner": d["rm_name"],
                "Product Mandate": d["product"],
                "Value (NGN)": fmt_ngn(d["value"]),
                "Stage": d["stage"],
                "Prob.": f"{d['prob']}%",
                "Exp. Close": d["close_date"],
                "Health": get_deal_health(d["due_date"], d["stage"]),
                "Next Action Due": f"{d['next_action']} (Due: {d['due_date']})"
            })
        
        df_display = pd.DataFrame(table_rows)
        st.dataframe(df_display, use_container_width=True, hide_index=True)

        # Expandable Activity Trail
        with st.expander("🕒 View Opportunity Activity Trail & Deal Audit"):
            for d in filtered_deals:
                st.markdown(f"**{d['id']} — {d['client_name']} ({d['company']}):**")
                for hist in d.get("history", []):
                    st.caption(f"• {hist}")
    else:
        st.info("No deals match the selected filters.")

# ==============================================================================
# SECTION 3: MANAGEMENT DASHBOARD (EXECUTIVE VIEW)
# ==============================================================================
if has_mgmt:
    with main_tab3:
        st.subheader("CFG Wealth Advisory Executive Management Dashboard")
        st.write("High-level governance telemetry, pipeline velocity, and advisor activity metrics.")

        all_deals = st.session_state["deals_db"]
        all_active = [d for d in all_deals if d["stage"] not in ["Won", "Lost"]]
        all_won = [d for d in all_deals if d["stage"] == "Won"]
        
        mgmt_pipe_total = sum([d["value"] for d in all_active])
        mgmt_pipe_weighted = sum([d["value"] * (d["prob"] / 100.0) for d in all_active])
        mgmt_won_total = sum([d["value"] for d in all_won])
        win_rate = (len(all_won) / len(all_deals) * 100) if len(all_deals) > 0 else 0

        # Management Top KPI Cards
        m_kpi1, m_kpi2, m_kpi3, m_kpi4, m_kpi5, m_kpi6 = st.columns(6)
        with m_kpi1:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">Pipeline Value</div><div class="kpi-value">{fmt_ngn(mgmt_pipe_total)}</div></div>', unsafe_allow_html=True)
        with m_kpi2:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">Weighted Value</div><div class="kpi-value">{fmt_ngn(mgmt_pipe_weighted)}</div></div>', unsafe_allow_html=True)
        with m_kpi3:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">Active Deals</div><div class="kpi-value">{len(all_active)}</div></div>', unsafe_allow_html=True)
        with m_kpi4:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">Proposals Logged</div><div class="kpi-value">{len([d for d in all_deals if d["stage"] in ["Proposal Sent", "Negotiation", "Won"]])}</div></div>', unsafe_allow_html=True)
        with m_kpi5:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">Won Volume</div><div class="kpi-value">{fmt_ngn(mgmt_won_total)}</div></div>', unsafe_allow_html=True)
        with m_kpi6:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">Win Rate</div><div class="kpi-value">{win_rate:.1f}%</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Section: Follow-ups Requiring Executive Attention
        st.markdown("### ⚠️ Follow-ups Requiring Attention (At Risk & Stalled Deals)")
        attention_deals = [d for d in all_active if get_deal_health(d["due_date"], d["stage"]) in ["🟡 At Risk", "🔴 Stalled"]]
        
        if attention_deals:
            att_rows = []
            for d in attention_deals:
                att_rows.append({
                    "Status": get_deal_health(d["due_date"], d["stage"]),
                    "Client": f"{d['client_name']} ({d['company']})",
                    "RM Owner": d["rm_name"],
                    "Mandate Value": fmt_ngn(d["value"]),
                    "Stage": d["stage"],
                    "Due Date": d["due_date"],
                    "Pending Next Action": d["next_action"]
                })
            st.dataframe(pd.DataFrame(att_rows), use_container_width=True, hide_index=True)
        else:
            st.success("All active deals have current follow-up schedules.")

        st.markdown("---")

        # Two-Column Analytic Breakdowns
        dash_col1, dash_col2 = st.columns(2)

        with dash_col1:
            st.markdown("### 👤 Pipeline Performance by RM")
            rm_summary = []
            for rm in set([d["rm_name"] for d in all_deals]):
                rm_d = [d for d in all_deals if d["rm_name"] == rm]
                rm_active = [d for d in rm_d if d["stage"] not in ["Won", "Lost"]]
                rm_won = [d for d in rm_d if d["stage"] == "Won"]
                
                rm_summary.append({
                    "RM Advisor": rm,
                    "Total Deals": len(rm_d),
                    "Pipeline (NGN)": fmt_ngn(sum([d["value"] for d in rm_active])),
                    "Weighted (NGN)": fmt_ngn(sum([d["value"] * (d["prob"]/100.0) for d in rm_active])),
                    "Won Value (NGN)": fmt_ngn(sum([d["value"] for d in rm_won]))
                })
            st.dataframe(pd.DataFrame(rm_summary), use_container_width=True, hide_index=True)

        with dash_col2:
            st.markdown("### 🏛️ Pipeline Distribution by Product")
            prod_summary = []
            for pr in set([d["product"] for d in all_deals]):
                pr_d = [d for d in all_deals if d["product"] == pr]
                pr_active = [d for d in pr_d if d["stage"] not in ["Won", "Lost"]]
                pr_won = [d for d in pr_d if d["stage"] == "Won"]

                prod_summary.append({
                    "Product Category": pr,
                    "Opportunities": len(pr_d),
                    "Active Volume": fmt_ngn(sum([d["value"] for d in pr_active])),
                    "Won Volume": fmt_ngn(sum([d["value"] for d in pr_won]))
                })
            st.dataframe(pd.DataFrame(prod_summary), use_container_width=True, hide_index=True)

        # Stage Breakdown Table
        st.markdown("### 📊 Deal Stage Distribution")
        stages = ["New", "Qualified", "Proposal Sent", "Negotiation", "Won", "Lost"]
        stage_summary = []
        for s in stages:
            s_deals = [d for d in all_deals if d["stage"] == s]
            stage_summary.append({
                "Stage": s,
                "Count": len(s_deals),
                "Total Value": fmt_ngn(sum([d["value"] for d in s_deals])),
                "Weighted Value": fmt_ngn(sum([d["value"] * (d["prob"]/100.0) for d in s_deals])) if s not in ["Won", "Lost"] else fmt_ngn(sum([d["value"] for d in s_deals]))
            })
        st.dataframe(pd.DataFrame(stage_summary), use_container_width=True, hide_index=True)
