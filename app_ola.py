# Channel Delivery Choice (Placed above the diagnostic form)
st.subheader("1. How would you like to receive your report?")
delivery_method = st.radio(
    "Select your preferred delivery channel:",
    ["📲 Send via WhatsApp", "✉️ Send via Email"],
    horizontal=True
)

with st.form("diagnostic_form"):
    user_name = st.text_input("Full Name *", placeholder="e.g. Amaka Adebayo")
    
    # Conditionally display the selected contact requirement
    if "WhatsApp" in delivery_method:
        user_phone = st.text_input("WhatsApp Number *", placeholder="e.g. +234 801 234 5678")
        user_email = ""
    else:
        user_email = st.text_input("Email Address *", placeholder="e.g. amaka@example.com")
        user_phone = ""

    st.subheader("2. Financial Health Assessment")
    earner_type = st.selectbox(
        "What best describes your current career / earning stage?",
        [
            "Early Career Professional (Building foundation & monthly saving habits)", 
            "Mid-Level / Senior Professional (Surplus cash looking for high-yield passive returns)", 
            "Business Owner / Entrepreneur (Managing business cashflow & personal wealth)", 
            "High-Net-Worth Individual (Preserving capital, hedging inflation & dollar assets)"
        ]
    )
    
    primary_goal = st.selectbox(
        "What is your primary financial focus right now?",
        [
            "Building a 6-Month Emergency Buffer & Strict Monthly Budget", 
            "Investing in Eurobonds, FGN Sukuk & Global Dollar Fixed Income", 
            "Clearing High-Interest Debts & Structuring Cashflow Habits", 
            "Scaling a Multi-Asset Investment Portfolio & Accessing Private Deals"
        ]
    )
    
    biggest_challenge = st.selectbox(
        "What is your biggest financial hurdle?",
        [
            "Confused by financial jargon and complex market terminology", 
            "Lack of time to research and analyze vetted investment deals", 
            "Inconsistency in execution, impulse spending, and lack of budgeting structure", 
            "Need for a high-caliber private wealth network and live accountability"
        ]
    )
    
    submitted = st.form_submit_button("Generate & Deliver My Action Plan 🚀")

# Strict Validation Logic
if submitted:
    if not user_name.strip():
        st.error("Please provide your full name.")
    elif "WhatsApp" in delivery_method and not user_phone.strip():
        st.error("Please enter your WhatsApp Number to receive your report.")
    elif "Email" in delivery_method and (not user_email.strip() or "@" not in user_email):
        st.error("Please enter a valid Email Address to receive your report.")
    else:
        # Proceed with OpenAI generation and show the direct 1-click dispatch for their chosen channel
        ...
