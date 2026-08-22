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

# Custom Corporate CSS (Fixed clean layout, no bottom glitches)
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
    .box-followup { border: 1.5px solid #F59E0B; }
    </style>
""", unsafe_allow_html=True)

# Shared Pipeline State
if "deals_pipeline" not in st.session_state:
    st.session_state["deals_pipeline"] = [
        {
            "Timestamp": "2026-08-22 10:30",
            "Client / Entity": "Alhaji Garba (Crestline Ventures)",
            "Module Source": "Module 2: Negotiation Desk",
            "Product Mandate": "CFG AM Naira Fixed Income Fund",
            "Capital Size": "₦150,000,000",
            "Stage": "Negotiation",
            "Days Inactive": 7
        },
        {
            "Timestamp": "2026-08-21 14:15",
            "Client / Entity": "Dr. Florence Adeleke (MedEquip)",
            "Module Source": "Module 1: Mandate Structuring",
            "Product Mandate": "CFG Multi-Currency Placement (USD)",
            "Capital Size": "$75,000 USD",
            "Stage": "Proposal Dispatched",
            "Days Inactive": 14
        },
        {
            "Timestamp": "2026-08-19 11:00",
            "Client / Entity": "Tariq Global Waqf",
            "Module Source": "Module 1: Mandate Structuring",
            "Product Mandate": "Halal Sukuk & Ijarah Portfolio",
            "Capital Size": "₦300,000,000",
            "Stage": "Mandate Approved",
            "Days Inactive": 3
        }
    ]

# Header
st.markdown('<span class="suite-badge">CRE8INTECH ENTERPRISE SUITE</span>', unsafe_allow_html=True)
st.title("🏛️ CFG Unified RM Wealth & Deal Suite")
st.caption("Institutional Portfolio Structuring, Objection Resolution & Follow-Up Strategy Desk")

api_key = st.secrets.get("OPENAI_API_KEY", "")

# 3 Focused Modules
tab1, tab2, tab3 = st.tabs([
    "📊 Module 1: Institutional Portfolio Diagnostician", 
    "🥊 Module 2: RM Negotiate & Battle Desk",
    "📈 Module 3: Deal Tracker & Follow-Up Strategy Desk"
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
                st.session_state["current_m1_client"] = client_profile
                st.session_state["current_m1_cap"] = f"{naira_capital} + {fx_capital}"

    if st.session_state.get("diag_calculated"):
        st.markdown("### 📋 Structured Portfolio Mandate & Tear-Sheet")
        st.markdown('<div class="output-box box-memo">', unsafe_allow_html=True)
        st.markdown(st.session_state["diag_output"])
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Log Mandate to Deal Tracker ✅"):
            st.session_state["deals_pipeline"].insert(0, {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Client / Entity": st.session_state.get("current_m1_client", "Corporate Client"),
                "Module Source": "Module 1: Mandate Structuring",
                "Product Mandate": "Blended Portfolio Allocation",
                "Capital Size": st.session_state.get("current_m1_cap", "₦150M"),
                "Stage": "Mandate Diagnosed",
                "Days Inactive": 0
            })
            st.success(" Mandate Logged. Available in Module 3 (Deal Tracker).")

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
            Client: {target_entity} | Product: {active_product} | Objection: {objection_type} | Context: {deal_context}

            OUTPUT FORMAT:
            1. 🥊 **Objection Resolution & Strategic Angles:** Exactly 3 sharp, compliance-aligned counter-arguments addressing the objection.
            2. 💼 **Internal Deal Summary:** 2-line strategic deal note.
            3. 🎯 **Recommended Next Action:** Practical next step for the RM.
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

                st.session_state["m2_target"] = target_entity
                st.session_state["m2_product"] = active_product
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
                st.session_state["deals_pipeline"].insert(0, {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Client / Entity": st.session_state.get("m2_target", "Target Client"),
                    "Module Source": "Module 2: Negotiation Desk",
                    "Product Mandate": st.session_state.get("m2_product", "CFG Placement"),
                    "Capital Size": "₦150,000,000",
                    "Stage": "Proposal Dispatched",
                    "Days Inactive": 0
                })
                st.rerun()
        else:
            st.success(" Deal Logged to Tracker. Instant Dispatch Channels Unlocked Below:")
            
            client_name_safe = st.session_state.get("m2_target", "Client")
            encoded_wa = urllib.parse.quote(st.session_state["whatsapp_text"])
            encoded_email_body = urllib.parse.quote(st.session_state["email_text"])
            encoded_subject = urllib.parse.quote(f"CFG Africa Investment Mandate Proposal - {client_name_safe}")

            btn_col1, btn_col2, btn_col3 = st.columns(3)

            with btn_col1:
                st.markdown(
                    f'<a href="https://wa.me/?text={encoded_wa}" target="_blank" class="action-btn-whatsapp">📲 Open in WhatsApp</a>', 
                    unsafe_allow_html=True
                )

            with btn_col2:
                st.markdown(
                    f'<a href="mailto:?subject={encoded_subject}&body={encoded_email_body}" class="action-btn-email">✉️ Open in Email App</a>', 
                    unsafe_allow_html=True
                )

            with btn_col3:
                st.download_button(
                    label="📄 Export Mandate Document",
                    data=st.session_state["email_text"],
                    file_name=f"CFG_Mandate_{client_name_safe.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

# ==============================================================================
# MODULE 3: DEAL TRACKER & FOLLOW-UP STRATEGY DESK
# ==============================================================================
with tab3:
    st.subheader("CFG Wealth Advisory Deal Tracker & Follow-Up Strategy Desk")
    st.write("Review all logged mandates and generate tailored re-engagement strategies for stalling or pending deals.")

    # Section 1: Active Deal Pipeline Table
    st.markdown("### 📋 Logged Opportunities Pipeline")
    df_pipeline = pd.DataFrame(st.session_state["deals_pipeline"])
    st.dataframe(df_pipeline, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Section 2: Interactive Follow-Up Strategy Generator
    st.subheader("🎯 Generate Tailored Re-Engagement Follow-Up")
    st.write("Generate a strategic follow-up message based on deal stall duration and client response context.")

    client_options = [d["Client / Entity"] for d in st.session_state["deals_pipeline"]]
    
    with st.form("followup_generator_form"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            selected_client = st.selectbox("Select Pending Client Deal:", client_options)
            inactivity_period = st.selectbox(
                "Time Elapsed Since Last Contact:",
                [
                    "3 to 5 Days (Gentle Prompt / Additional Insight)",
                    "1 to 2 Weeks (Value-Add Yield Update / Market Shift)",
                    "3+ Weeks (Executive Re-Engagement / Alternative Structure)"
                ]
            )
        with col_f2:
            client_status = st.selectbox(
                "Current Client Response Status:",
                [
                    "No Response / Deal Inactive after initial proposal",
                    "Client requested more time to consult Investment Committee/Board",
                    "Client comparing with competing commercial bank rate",
                    "Client awaiting dividend/liquidity inflow before committing"
                ]
            )
            strategy_angle = st.text_input("Specific Angle to Emphasize:", value="Highlight current SEC money market fund yield benchmark and compounding advantage.")

        submit_followup = st.form_submit_button("Generate Follow-Up Strategy & Messages ⚡")

    if submit_followup:
        if not api_key:
            st.error("Please add OPENAI_API_KEY to Streamlit Secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt_followup = f"""
            You are the Senior Wealth Advisor Copilot at CFG Africa (MD: Babajide Lawani).
            
            CLIENT DEAL: {selected_client}
            TIME ELAPSED: {inactivity_period}
            CURRENT STATUS: {client_status}
            STRATEGIC FOCUS: {strategy_angle}

            DELIVER A HIGH-CONVERSION RE-ENGAGEMENT PACKAGE:
            1. 🎯 **Strategic Follow-Up Angle:** Concise tactical guidance for the RM (why this approach works without sounding pushy).
            2. 📱 **Ready-to-Send WhatsApp Follow-Up:** Clean, polite, high-impact bulleted message. Include CFG Africa sign-off.
            3. ✉️ **Formal Follow-Up Email Body:** Boardroom-ready re-engagement note with relevant market/yield context.
            """
            with st.spinner("Generating Follow-Up Strategy..."):
                res_f = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_followup}]
                )
                st.session_state["followup_res"] = res_f.choices[0].message.content
                st.session_state["followup_client"] = selected_client
                st.session_state["followup_done"] = True

    if st.session_state.get("followup_done"):
        st.markdown(f"### 🚀 Follow-Up Action Plan for **{st.session_state.get('followup_client')}**")
        st.markdown('<div class="output-box box-followup">', unsafe_allow_html=True)
        st.markdown(st.session_state["followup_res"])
        st.markdown('</div>', unsafe_allow_html=True)
