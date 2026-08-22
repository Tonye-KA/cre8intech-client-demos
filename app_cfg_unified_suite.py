import streamlit as st
import openai

# Page Configuration
st.set_page_config(
    page_title="CFG Enterprise Wealth Suite | CFG Africa",
    page_icon="🏛️",
    layout="wide"
)

# Custom Corporate CSS (CFG Navy, Precision Slate & Emerald Teal)
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
        padding-top: 2rem !important;
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

    /* Output Section Containers */
    .output-box {
        background-color: #0F172A;
        border-radius: 10px;
        padding: 22px;
        margin-top: 16px;
        margin-bottom: 16px;
    }

    .box-memo {
        border: 1.5px solid #38BDF8;
    }

    .box-whatsapp {
        border: 1.5px solid #22C55E;
    }

    .box-email {
        border: 1.5px solid #F59E0B;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<span class="suite-badge">CRE8INTECH ENTERPRISE SUITE</span>', unsafe_allow_html=True)
st.title("🏛️ CFG Unified RM Wealth & Deal Suite")
st.caption("Institutional Portfolio Diagnostic, Multi-Currency Structuring & Live Battle Card Engine")

api_key = st.secrets.get("OPENAI_API_KEY", "")

# Two Interlinked RM Workflows
tab1, tab2 = st.tabs([
    "📊 Module 1: Institutional RM Mandate Diagnostician", 
    "🥊 Module 2: RM Negotiate & Battle Card Desk"
])

# ==============================================================================
# MODULE 1: INSTITUTIONAL RM MANDATE DIAGNOSTICIAN
# ==============================================================================
with tab1:
    st.subheader("Institutional Portfolio Diagnostician & Mandate Builder")
    st.write("Advanced structuring tool for Wealth Advisors during high-ticket corporate and HNWI mandate onboarding.")

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
        submit_diag = st.form_submit_button("Generate Institutional Mandate Strategy 📊")

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

            DELIVER A BOARDROOM-READY MANDATE REPORT DIVIDED INTO 3 CLEAR SECTIONS:
            1. 💼 **Executive Mandate Thesis:** Concise 2-line strategic allocation summary.
            2. 🏛️ **Structured Portfolio Allocation Breakdown:**
               - Exact % and nominal amounts across CFG AM Naira Fixed Income Fund, Multi-Currency Placements, Commercial Papers, and Halal Sukuk Notes.
            3. 📋 **Investment Committee Internal Tear-Sheet:** Clean bulleted brief the RM can submit directly to management or log in the CRM.
            """
            with st.spinner("Calculating Institutional Mandate..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_diag}]
                )
                st.markdown('<div class="output-box box-memo">', unsafe_allow_html=True)
                st.markdown(res.choices[0].message.content)
                st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# MODULE 2: RM NEGOTIATE & BATTLE CARD DESK (3 COMMUNICATION LAYERS)
# ==============================================================================
with tab2:
    st.subheader("Live Deal-Closer & Multi-Channel Negotiation Desk")
    st.write("Generates instant objection battle cards and client-ready outputs across 3 distinct communication layers.")

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

        submit_battle = st.form_submit_button("Generate Battle Card & Multi-Layer Proposals ⚡")

    if submit_battle:
        if not api_key:
            st.error("Please add OPENAI_API_KEY to Streamlit Secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            
            prompt_layer1 = f"""
            You are the Senior Sales Enablement Copilot at CFG Africa (MD: Babajide Lawani).
            Generate the RM Battle Card & Internal Tear-Sheet for:
            Client: {target_entity} | Product: {active_product} | Objection: {objection_type} | Context: {deal_context}

            OUTPUT:
            - Exactly 3 sharp, compliance-vetted institutional counter-arguments addressing the objection (highlighting SEC liquidity, active duration management, and tax alpha).
            - A quick Internal Deal Log Tear-Sheet for CRM records.
            """

            prompt_layer2 = f"""
            You are drafting a client-facing WhatsApp briefing for a Relationship Manager at CFG Africa.
            Client: {target_entity} | Product: {active_product} | Context: {deal_context}

            OUTPUT:
            A clean, executive WhatsApp message using professional bullet points.
            Include a warm opening, structured allocation highlight, next steps, and official sign-off:
            ───────────────────────────────
            🏛️ CFG Africa | Wealth Management & Advisory
            Regulated by the Securities & Exchange Commission (SEC)
            Website: https://cfgafrica.com
            ───────────────────────────────
            """

            prompt_layer3 = f"""
            You are drafting a formal Boardroom-Ready Corporate Email Proposal from CFG Africa to:
            Client: {target_entity} | Product: {active_product} | Context: {deal_context}

            OUTPUT:
            A complete corporate email with Subject line, executive greeting, strategic rationale, regulatory safeguards, and account onboarding instructions.
            """

            with st.spinner("Generating Multi-Layer Deal Package..."):
                # Layer 1 Call
                res1 = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_layer1}]
                )
                # Layer 2 Call
                res2 = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_layer2}]
                )
                # Layer 3 Call
                res3 = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_layer3}]
                )

                st.success("Multi-Layer Deal Package Successfully Generated:")

                # Display Layer 1: Internal Battle Card & Memo
                st.markdown("### 🥊 Layer 1: RM Battle Card & Internal Client Memo")
                st.markdown('<div class="output-box box-memo">', unsafe_allow_html=True)
                st.markdown(res1.choices[0].message.content)
                st.markdown('</div>', unsafe_allow_html=True)

                # Display Layer 2: WhatsApp Executive Briefing
                st.markdown("### 📱 Layer 2: Executive WhatsApp Briefing (Client Mobile)")
                st.markdown('<div class="output-box box-whatsapp">', unsafe_allow_html=True)
                st.markdown(res2.choices[0].message.content)
                st.markdown('</div>', unsafe_allow_html=True)

                # Display Layer 3: Formal Email Proposal
                st.markdown("### ✉️ Layer 3: Boardroom-Ready Proposal (Corporate Email)")
                st.markdown('<div class="output-box box-email">', unsafe_allow_html=True)
                st.markdown(res3.choices[0].message.content)
                st.markdown('</div>', unsafe_allow_html=True)
