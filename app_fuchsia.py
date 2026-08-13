import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Fuchsia AI Concierge | Fuchsia Desserts", 
    page_icon="🍰", 
    layout="centered"
)

# Custom High-End Styling (Signature Fuchsia Pink & Pure White - No Yellow)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Montserrat:wght@400;500;600;700&display=swap');

    /* Force Pure White Canvas & Override Streamlit Yellow Defaults */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Headings */
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

    /* Cre8intech Badge Header */
    .demo-badge {
        background-color: #D946EF !important; /* Fuchsia Pink */
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

    /* FORCE ALL DROPDOWN CONTAINERS TO BE WHITE/PINK (OVERRIDE YELLOW) */
    div[data-baseweb="select"], 
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1.5px solid #D946EF !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] * {
        color: #1A1A1A !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    div[data-baseweb="select"] svg {
        fill: #D946EF !important;
    }

    /* DROPDOWN POPUP MENU (LIST OF OPTIONS) - REMOVE ALL YELLOW HOVER/BG */
    ul[role="listbox"],
    div[data-baseweb="menu"],
    div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #D946EF !important;
        border-radius: 8px !important;
    }

    ul[role="listbox"] li,
    div[data-baseweb="menu"] div,
    div[data-baseweb="popover"] div {
        color: #1A1A1A !important;
        background-color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
    }

    /* Pink Hover Effect for Options */
    ul[role="listbox"] li:hover,
    div[data-baseweb="menu"] div:hover,
    div[data-baseweb="popover"] div:hover {
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
        margin-top: 15px !important;
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
st.write("Welcome! Learn about the **health & ingredient benefits** of our desserts or plan custom **event catering & luxury gifts**.")

# System Instructions
SYSTEM_PROMPT = """
You are the friendly, welcoming 'Fuchsia AI Concierge' for Fuchsia Desserts (Founder: Tosan).
Speak in a warm, candid, friendly tone—like an encouraging expert friend! Avoid overly complicated medical or technical terms.

CORE PRINCIPLE:
Every single dessert product at Fuchsia Desserts falls into a legitimate health and ingredient goal!
- Cocoa/Dark Chocolate = Heart health, circulation, mood-boosting endorphins, and antioxidants.
- Fruits & Berries = Immune support, skin glow, vitamins, and natural digestion.
- Nuts & Seeds = Healthy fats, sustained energy, muscle recovery, and brain focus.
- Low-Sugar/Keto/Gluten-Free = Weight management, balanced blood sugar, and gut comfort.

Your Job:
1. Educate the user on the specific health benefits of the product or goal they selected in plain, friendly English.
2. Recommend specific, delicious Fuchsia Desserts items that fit.
3. For events and gifts, ALSO explain the wholesome health/ingredient benefits of the curated package so the recipient feels pampered and nourished.
"""

# 2 Merged Tabs
tab1, tab2 = st.tabs(["🌿 Health Benefits & Product Matcher", "🎉 Event & Gift Concierge"])

api_key = st.secrets.get("OPENAI_API_KEY", "")

# --- TAB 1: Health Benefits & Product Matcher ---
with tab1:
    with st.form("health_form"):
        st.subheader("Discover Ingredient Benefits & Find Your Match")
        
        product_choice = st.selectbox(
            "1. Discover the health benefits of a specific product:",
            [
                "All Products / Let AI Recommend Based on Health Goal",
                "Signature Dark Chocolate Cakes & Gateaux",
                "Artisanal Fresh Berry & Fruit Tarts",
                "Gourmet Parfaits & Layered Mousse Cups",
                "Nut & Seed Energy Bites & Protein Treats",
                "Low-Sugar & Keto-Friendly Dessert Box",
                "Gluten-Free & Dairy-Free Artisan Pastries"
            ]
        )
        
        health_focus = st.selectbox(
            "2. Or match your specific health goal:",
            [
                "Healthy Heart & Good Circulation (Rich Dark Cocoa & Flavonoids)",
                "Clean & Sustained Energy (Nuts, Seeds & Healthy Fats)",
                "Low Sugar & Guilt-Free Sweet Craving (Balanced Blood Sugar)",
                "Easy Digestion & Light Stomach (Gluten-Free / Dairy-Free)",
                "Strong Bones & Overall Body Vitality (Clean Wholesome Minerals)",
                "Mood Boost & Stress Relief (Natural Endorphins & Magnesium)",
                "Immune Support & Glowing Skin (Antioxidant Berries & Fruits)"
            ]
        )
        
        submit_health = st.form_submit_button("Explain Health Benefits & Match Product ✨")

    if submit_health:
        if not api_key:
            st.error("Please configure OPENAI_API_KEY in Streamlit secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"In a warm, candid, and friendly tone, educate the customer on the health benefits of Fuchsia Desserts for: Product Selected = {product_choice}, Health Goal = {health_focus}. Explain clearly how the wholesome ingredients support their health and recommend specific items to order."
            
            with st.spinner("Analyzing ingredient health benefits..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
                )
                st.success("Your Health & Ingredient Analysis:")
                st.markdown(res.choices[0].message.content)

# --- TAB 2: Combined Event & Gift Concierge ---
with tab2:
    with st.form("event_gift_form"):
        st.subheader("Plan Events or Luxury Gifts")
        
        purpose = st.selectbox(
            "1. What are you planning today?",
            [
                "Event Catering (Weddings, Galas & Large Parties)",
                "Private Dinner / Small Gathering Dessert Table",
                "Corporate Client / Executive VIP Gift Box",
                "Birthday / Celebration Gift Hamper"
            ]
        )
        
        guest_count = st.selectbox(
            "2. How many people are you serving or gifting?",
            [
                "1 - 2 People (Intimate Treat / Single Gift)",
                "3 - 6 People (Small Group / Gift Hamper)",
                "7 - 20 People (Party Box / Small Event)",
                "20+ People (Large Event / Bulk Corporate Gifting)"
            ]
        )
        
        submit_event_gift = st.form_submit_button("Curate Event Plan & Explain Benefits 🎁")

    if submit_event_gift:
        if not api_key:
            st.error("Please configure OPENAI_API_KEY in Streamlit secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Curate an event dessert plan or gift box for Fuchsia Desserts: Purpose = {purpose}, Size = {guest_count}. Provide menu choices, platter/box quantities, and MANDATORY: educate them on the health and wholesome ingredient benefits of the curated package so their guests/recipients enjoy guilt-free luxury."
            
            with st.spinner("Curating your custom plan..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
                )
                st.success("Your Custom Event & Gift Package:")
                st.markdown(res.choices[0].message.content)
