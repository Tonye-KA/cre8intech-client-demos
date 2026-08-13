import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Fuchsia AI Health Concierge | Fuchsia Desserts", 
    page_icon="🍰", 
    layout="centered"
)

# Custom High-End Styling (Signature Fuchsia Pink & Pure White - Overrides Global Config)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Montserrat:wght@400;500;600;700&display=swap');

    /* FORCE FULL PAGE CANVAS TO PURE WHITE */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], .stApp {
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

    /* DROPDOWN CONTAINERS (FORCE FUCHSIA & WHITE) */
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

    /* DROPDOWN POPUP MENU (OVERRIDE YELLOW HOVER STATES) */
    ul[role="listbox"],
    div[data-baseweb="menu"],
    div[data-baseweb="popover"],
    div[role="listbox"] {
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
    div[data-baseweb="popover"] div:hover,
    [aria-selected="true"] {
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
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #6B7280 !important;
    }

    button[aria-selected="true"] div p {
        color: #D946EF !important;
    }

    /* ACTION BUTTON: Signature Fuchsia Pink */
    div.stButton > button,
    button[kind="primary"],
    button[kind="secondary"] {
        background-color: #D946EF !important; /* FUCHSIA PINK */
        background-image: none !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 14px 20px !important;
        width: 100% !important;
        margin-top: 15px !important;
        box-shadow: 0px 4px 14px rgba(217, 70, 239, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button *,
    button[kind="primary"] *,
    button[kind="secondary"] * {
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
st.title("🍰 Fuchsia AI Health Concierge")
st.caption("Configured for **Fuchsia Desserts** (Founder: Tosan)")
st.write("Welcome! I am **Fuchsia**, your AI health concierge. Discover the **health benefits** of our desserts or plan custom **event catering & luxury gifts**.")

# System Instructions
SYSTEM_PROMPT = """
You are 'Fuchsia', the friendly and knowledgeable AI Health Concierge for Fuchsia Desserts (Founder: Tosan).
Introduce yourself warmly as 'Fuchsia'. Speak in a candid, encouraging, expert tone. Avoid heavy medical or technical jargon.

CORE PRINCIPLE:
Every single dessert product at Fuchsia Desserts connects to a real health and ingredient benefit!
- Dark Chocolate/Cocoa = Heart circulation, mood-boosting endorphins, and rich antioxidants.
- Berries & Fruits = Immune support, skin glow, vitamins, and natural digestion.
- Nuts & Seeds = Healthy fats, sustained physical energy, and brain focus.
- Low-Sugar/Keto/Gluten-Free = Balanced blood sugar, weight management, and digestive comfort.

Your Job:
1. Educate the user on the specific health benefits of the product or goal they selected in plain, friendly terms.
2. Recommend specific, delicious Fuchsia Desserts items that fit.
3. For events and gifts, curate tailored dessert packages, quantities, and presentation ideas while highlighting the wholesome health benefits.
"""

# 3 Separated Tabs
tab1, tab2, tab3 = st.tabs(["🌿 Health Benefit Finder", "🎉 Event Catering Planner", "🎁 Luxury Gift Assistant"])

api_key = st.secrets.get("OPENAI_API_KEY", "")

# --- TAB 1: Health Benefits and Product Matcher ---
with tab1:
    with st.form("health_matcher_form"):
        st.subheader("Health Benefits and Product Matcher")
        
        product_choice = st.selectbox(
            "1. Discover the health benefits of a specific product:",
            [
                "All Products / Recommend Based on Health Goal",
                "Signature Dark Chocolate Cakes & Gateaux",
                "Artisanal Fresh Berry & Fruit Tarts",
                "Gourmet Parfaits & Layered Mousse Cups",
                "Nut & Seed Energy Bites & Protein Treats",
                "Low-Sugar & Keto-Friendly Dessert Box",
                "Gluten-Free & Dairy-Free Artisan Pastries"
            ]
        )
        
        health_focus = st.selectbox(
            "2. Or select your specific health goal:",
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
        
        submit_health = st.form_submit_button("Explain Health Benefits & Match Dessert ✨")

    if submit_health:
        if not api_key:
            st.error("Please configure OPENAI_API_KEY in Streamlit secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Introduce yourself as Fuchsia, the AI Health Concierge. Educate the customer on the health benefits of Fuchsia Desserts for: Product Selected = {product_choice}, Health Goal = {health_focus}. Explain clearly how the wholesome ingredients support their health and recommend specific items."
            
            with st.spinner("Fuchsia is analyzing your health match..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
                )
                st.success("Your Health & Ingredient Recommendation:")
                st.markdown(res.choices[0].message.content)

# --- TAB 2: Event Catering Planner ---
with tab2:
    with st.form("event_form"):
        st.subheader("Plan Event & Party Catering")
        
        event_type = st.selectbox(
            "1. What type of event are you hosting?",
            [
                "Wedding Reception / Bridal Dessert Table",
                "Corporate Gala / Conference Catering",
                "Private Dinner Party / Intimate Gathering",
                "Birthday / Milestone Celebration"
            ]
        )
        
        guest_count = st.selectbox(
            "2. Estimated number of guests?",
            ["10 - 25 Guests (Intimate Gathering)", "26 - 50 Guests (Medium Party)", "51 - 100 Guests (Large Event)", "100+ Guests (Grand Event)"]
        )
        
        submit_event = st.form_submit_button("Plan My Event Dessert Menu 🎉")

    if submit_event:
        if not api_key:
            st.error("Please configure OPENAI_API_KEY in Streamlit secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Introduce yourself as Fuchsia. Create a friendly event dessert catering plan for Fuchsia Desserts: Event Type = {event_type}, Guest Count = {guest_count}. Detail menu choices, platter quantities, and explain the health benefits of the treats so guests enjoy guilt-free luxury."
            
            with st.spinner("Fuchsia is curating your event plan..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
                )
                st.success("Your Custom Event Catering Plan:")
                st.markdown(res.choices[0].message.content)

# --- TAB 3: Luxury Gift Assistant ---
with tab3:
    with st.form("gift_form"):
        st.subheader("Curate Luxury Dessert Gifts")
        
        gift_occasion = st.selectbox(
            "1. What is the gifting occasion?",
            [
                "Corporate Client / VIP Appreciation Box",
                "Birthday / Milestone Anniversary Gift",
                "Executive Thank You Hamper",
                "Get Well Soon / Mindful Wellness Gift"
            ]
        )
        
        gift_size = st.selectbox(
            "2. Select gift size preference:",
            ["Single Luxury Gift Box (1 - 2 People)", "Family / Small Team Gift Hamper (3 - 6 People)", "Bulk Executive Orders (Multiple Recipients)"]
        )
        
        submit_gift = st.form_submit_button("Curate Gift Package 🎁")

    if submit_gift:
        if not api_key:
            st.error("Please configure OPENAI_API_KEY in Streamlit secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Introduce yourself as Fuchsia. Curate a luxury dessert gift box for Fuchsia Desserts: Occasion = {gift_occasion}, Size = {gift_size}. Provide product selections, packaging style, and presentation details."
            
            with st.spinner("Fuchsia is curating your gift box..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
                )
                st.success("Your Curated Gift Package:")
                st.markdown(res.choices[0].message.content)
