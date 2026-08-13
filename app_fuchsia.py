import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Fuchsia AI Concierge | Fuchsia Desserts", 
    page_icon="🍰", 
    layout="centered"
)

# Custom High-End Styling (Signature Fuchsia Pink & Pure White Background)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Montserrat:wght@400;500;600;700&display=swap');

    /* Force Pure White Canvas */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #1A1A1A !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    p, span, label, div {
        color: #2D2D2D !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    .demo-badge {
        background-color: #D946EF !important; /* Signature Fuchsia Pink */
        color: #FFFFFF !important;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        display: inline-block;
        margin-bottom: 12px;
        text-transform: uppercase;
    }

    /* Container Card */
    div[data-testid="stForm"], div.stBlock {
        background-color: #FAFAFA !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 28px !important;
        box-shadow: 0px 4px 20px rgba(217, 70, 239, 0.05) !important;
    }

    /* DROPDOWNS */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
        padding: 6px !important;
    }

    div[data-baseweb="select"] * {
        color: #1A1A1A !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    div[data-baseweb="select"] svg {
        fill: #D946EF !important;
    }

    ul[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
    }

    ul[role="listbox"] li {
        color: #1A1A1A !important;
        background-color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    ul[role="listbox"] li:hover {
        background-color: #FDF4FF !important;
        color: #D946EF !important;
    }

    /* TABS STYLING */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        padding-bottom: 8px !important;
    }

    button[data-baseweb="tab"] div p {
        font-family: 'Playfair Display', serif !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #6B7280 !important;
    }

    button[aria-selected="true"] div p {
        color: #D946EF !important;
    }

    /* ACTION BUTTON: Signature Fuchsia Pink */
    div.stButton > button {
        background-color: #D946EF !important; /* FUCHSIA PINK */
        border-radius: 8px !important;
        border: none !important;
        padding: 14px 20px !important;
        width: 100% !important;
        margin-top: 10px !important;
        box-shadow: 0px 4px 14px rgba(217, 70, 239, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button * {
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }

    div.stButton > button:hover {
        background-color: #C026D3 !important;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<span class="demo-badge">CRE8INTECH PROTOTYPE DEMO</span>', unsafe_allow_html=True)
st.title("🍰 Fuchsia AI Concierge")
st.caption("Configured for **Fuchsia Desserts** (Founder: Tosan)")
st.write("Welcome! Find delicious treats matching your **health goals** or plan **party catering & luxury gifts** in seconds.")

# System Instructions
SYSTEM_PROMPT = """
You are the friendly 'Fuchsia AI Concierge' for Fuchsia Desserts (Founder: Tosan).
Speak in a warm, welcoming, candid, and friendly tone—like an encouraging expert friend! Avoid overly complicated medical or technical terms.

Your Job:
1. Explain the real health benefits of ingredients used in Fuchsia Desserts (e.g., dark cocoa antioxidants for heart health, natural fruit nutrients, low-sugar options, clean nuts for energy).
2. Recommend delicious Fuchsia Desserts that match their simple health goal.
3. Help customers plan event dessert tables or gift boxes with easy quantities and pairing suggestions.
"""

# 2 Merged Tabs
tab1, tab2 = st.tabs(["🌿 Healthy Dessert Finder", "🎉 Event & Gift Concierge"])

api_key = st.secrets.get("OPENAI_API_KEY", "")

# --- TAB 1: Healthy Dessert Finder ---
with tab1:
    with st.form("health_form"):
        st.subheader("Match Your Health Goal")
        
        health_focus = st.selectbox(
            "What health benefit or goal are you looking for today?",
            [
                "Healthy Heart & Good Circulation (Rich Dark Cocoa & Berries)",
                "Clean & Sustained Energy (Nuts, Seeds & Superfoods)",
                "Low Sugar & Guilt-Free Sweet Craving",
                "Easy Digestion & Light Ingredients (Gluten-Free / Dairy-Free)",
                "Strong Bones & Overall Wellbeing (Clean Wholesome Ingredients)"
            ]
        )
        
        submit_health = st.form_submit_button("Find My Healthy Dessert Match ✨")

    if submit_health:
        if not api_key:
            st.error("Please configure OPENAI_API_KEY in Streamlit secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"In a warm, candid, friendly tone, recommend 2-3 delicious Fuchsia Desserts for someone looking for: {health_focus}. Explain the health benefits in simple, welcoming terms without technical jargon."
            
            with st.spinner("Finding your healthy dessert match..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
                )
                st.success("Here are your recommended treats:")
                st.markdown(res.choices[0].message.content)

# --- TAB 2: Combined Event & Gift Concierge ---
with tab2:
    with st.form("event_gift_form"):
        st.subheader("Plan Events or Luxury Gifts")
        
        purpose = st.selectbox(
            "1. What are you planning today?",
            [
                "Event Catering (Weddings, Galas & Parties)",
                "Private Dinner / Small Gathering Dessert Table",
                "Corporate Client / Executive Gift Box",
                "Birthday / Celebration Gift Box"
            ]
        )
        
        guest_count = st.selectbox(
            "2. How many people are you serving or gifting?",
            ["1 - 2 People (Intimate Treat / Single Gift)", "3 - 6 People (Small Group / Gift Hamper)", "7 - 20 People (Party Box / Small Event)", "20+ People (Large Event / Bulk Corporate Gifting)"]
        )
        
        submit_event_gift = st.form_submit_button("Get Event & Gift Recommendations 🎁")

    if submit_event_gift:
        if not api_key:
            st.error("Please configure OPENAI_API_KEY in Streamlit secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Create a friendly, elegant recommendation for Fuchsia Desserts for: Purpose = {purpose}, Size = {guest_count}. Suggest menu choices, platter quantities or packaging ideas, and mention why it will delight their guests or recipient."
            
            with st.spinner("Curating your custom plan..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
                )
                st.success("Your Custom Event & Gift Plan:")
                st.markdown(res.choices[0].message.content)
