import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Fuchsia AI Concierge | Fuchsia Desserts", 
    page_icon="🍰", 
    layout="centered"
)

# Custom Styling (Fuchsia Desserts Minimalist Luxury Palette)
st.markdown("""
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Montserrat:wght@400;500;600;700&display=swap');

    /* Force Root Canvas & App Container to Pure White */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Remove Streamlit Header Padding Effects */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Luxurious Serif Typography for Titles */
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

    /* Cre8intech Badge Header - Sleek Fuchsia Badge */
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

    /* Container Card: Delicate Grey Border with Ultra-Soft Blush Glow */
    div[data-testid="stForm"], div.stBlock {
        background-color: #FAFAFA !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 28px !important;
        box-shadow: 0px 4px 20px rgba(217, 70, 239, 0.05) !important;
    }

    /* DROPDOWNS: Clean White Fields with Dark Text & Elegant Focus Border */
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
    }

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

    /* Dropdown Arrow Color */
    div[data-baseweb="select"] svg {
        fill: #D946EF !important;
    }

    /* Popup Options List */
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

    /* ACTION BUTTON: High-Contrast Fuchsia Button */
    div.stButton > button {
        background-color: #D946EF !important; /* Fuchsia Pink */
        border-radius: 8px !important;
        border: none !important;
        padding: 14px 20px !important;
        width: 100% !important;
        margin-top: 10px !important;
        box-shadow: 0px 4px 14px rgba(217, 70, 239, 0.25) !important;
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
st.write("Welcome! Discover artisanal treats tailored to your **dietary lifestyle** or curate a **thoughtful luxury gift / event platter** in seconds.")

# System Prompt
SYSTEM_PROMPT = """
You are the 'Fuchsia AI Concierge', an elegant, warm, and sophisticated virtual assistant for Fuchsia Desserts.
Your goal is to guide customers seamlessly whether they care about dietary wellness or luxury gifting.

RULES:
1. Always balance **Mindful Indulgence** (health/clean ingredients) with **Luxury Celebration** (gifting/events).
2. Highlight wholesome ingredient benefits (e.g., dark cocoa antioxidants, natural sweeteners, gluten-free choices, portion control).
3. Provide tailored, elegant dessert recommendations.
4. Keep output beautifully structured with bullet points and a warm, refined tone.
"""

# Tabs for 2 Primary Use-Cases
tab1, tab2 = st.tabs(["🥗 Health & Dietary Finder", "🎁 Gift & Event Assistant"])

api_key = st.secrets.get("OPENAI_API_KEY", "")

# --- TAB 1: Health & Dietary Assistant ---
with tab1:
    with st.form("health_form"):
        st.subheader("Mindful Indulgence Selector")
        
        diet_pref = st.selectbox(
            "What is your primary dietary preference?",
            ["Keto / Low-Carb", "Gluten-Free", "Low Sugar / Mindful Sweetness", "Dairy-Free Options", "Traditional Luxury Indulgence"]
        )
        
        health_goal = st.selectbox(
            "What ingredient benefit matters most to you?",
            ["High Antioxidants (Dark Cocoa & Berries)", "Natural Sweeteners Only", "Clean Nut & Fruit Ingredients", "Portion-Controlled Treats"]
        )
        
        submit_health = st.form_submit_button("Find My Healthy Match ✨")

    if submit_health:
        if not api_key:
            st.error("Please configure OPENAI_API_KEY in Streamlit secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Recommend a dessert experience for a customer seeking: Diet Preference = {diet_pref}, Key Ingredient Goal = {health_goal}. Explain the health/ingredient benefits elegantly and pitch Fuchsia Desserts."
            
            with st.spinner("Curating your mindful dessert selection..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
                )
                st.success("Your Personal Recommendation:")
                st.markdown(res.choices[0].message.content)

# --- TAB 2: Gift & Event Concierge ---
with tab2:
    with st.form("gift_form"):
        st.subheader("Luxury Gift & Event Selector")
        
        occasion = st.selectbox(
            "What is the occasion?",
            ["Birthday / Anniversary Gift", "Corporate Gifting", "Dinner Party Dessert Platter", "Personal Celebration Treat"]
        )
        
        guest_count = st.selectbox(
            "How many guests are you serving?",
            ["1 - 2 People (Intimate)", "3 - 6 People (Small Group)", "7 - 15 People (Party Box)", "15+ People (Corporate/Large Event)"]
        )
        
        submit_gift = st.form_submit_button("Recommend Gift Package 🎁")

    if submit_gift:
        if not api_key:
            st.error("Please configure OPENAI_API_KEY in Streamlit secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Recommend a dessert gift/event package for: Occasion = {occasion}, Serving Size = {guest_count}. Suggest pairing ideas, platter packaging, and a touch of health consciousness."
            
            with st.spinner("Curating your luxury gift recommendation..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
                )
                st.success("Your Curated Gift Recommendation:")
                st.markdown(res.choices[0].message.content)
