import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Fuchsia Health Concierge | Fuchsia Desserts", 
    page_icon="🍰", 
    layout="centered"
)

# Custom High-End Styling (Signature Fuchsia Pink & Pure White - Compact & Clean)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Montserrat:wght@400;500;600;700&display=swap');

    /* Full Page Canvas to Pure White */
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
        background-color: #D946EF !important;
        color: #FFFFFF !important;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.5px;
        display: inline-block;
        margin-bottom: 10px;
        text-transform: uppercase;
    }

    /* Compact Form Card */
    div[data-testid="stForm"], div.stBlock {
        background-color: #FAFAFA !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0px 4px 16px rgba(217, 70, 239, 0.04) !important;
        margin-bottom: 16px !important;
    }

    /* COMPACT DROPDOWN SELECTORS (REMOVED EXTRA HEIGHT/SPACE) */
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1.5px solid #D946EF !important;
        border-radius: 8px !important;
        padding: 2px 8px !important;
        min-height: 40px !important;
    }

    div[data-baseweb="select"] * {
        color: #1A1A1A !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
    }

    div[data-baseweb="select"] svg {
        fill: #D946EF !important;
    }

    /* POPUP MENU */
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
        font-size: 13px !important;
    }

    ul[role="listbox"] li:hover,
    div[data-baseweb="menu"] div:hover,
    div[data-baseweb="popover"] div:hover,
    [aria-selected="true"] {
        background-color: #FDF4FF !important;
        color: #D946EF !important;
    }

    /* NATURAL, CLEAN TAB BAR (NO SQUEEZING, NO CLIPPING) */
    div[data-baseweb="tab-list"],
    div[data-testid="stTabs"] > div:first-child {
        display: flex !important;
        justify-content: flex-start !important;
        border-bottom: 1.5px solid #F3E8FF !important;
        gap: 16px !important;
        padding-bottom: 4px !important;
    }

    button[data-baseweb="tab"],
    div[data-testid="stTabs"] button {
        flex: 0 0 auto !important;
        background-color: transparent !important;
        border: none !important;
        padding: 6px 10px !important;
        cursor: pointer !important;
    }

    button[data-baseweb="tab"] div p,
    div[data-testid="stTabs"] button p {
        font-family: 'Playfair Display', serif !important;
        font-size: 14.5px !important;
        font-weight: 700 !important;
        color: #6B7280 !important;
        white-space: nowrap !important;
    }

    button[aria-selected="true"] div p,
    div[data-testid="stTabs"] button[aria-selected="true"] p {
        color: #D946EF !important;
    }

    /* SLEEK & COMPACT PINK BUTTON */
    div.stButton > button,
    button[kind="primaryFormSubmit"],
    button[kind="secondaryFormSubmit"],
    button[data-testid="stFormSubmitButton"] > button {
        background-color: #D946EF !important;
        background-image: none !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 22px !important;
        width: auto !important;
        min-width: 260px !important;
        max-width: 340px !important;
        margin-top: 10px !important;
        box-shadow: 0px 4px 12px rgba(217, 70, 239, 0.25) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button *,
    button[kind="primaryFormSubmit"] *,
    button[kind="secondaryFormSubmit"] *,
    button[data-testid="stFormSubmitButton"] > button * {
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }

    div.stButton > button:hover,
    button[kind="primaryFormSubmit"]:hover,
    button[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #C026D3 !important;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<span class="demo-badge">CRE8INTECH PROTOTYPE DEMO</span>', unsafe_allow_html=True)
st.title("🍰 Fuchsia Health Concierge")
st.caption("Configured for **Fuchsia Desserts** (Founder: Tosan)")
st.write("Welcome! I am **Fuchsia**, your health concierge. Discover the **health benefits** of our desserts or plan custom **event catering & luxury gifts**.")

# System Instructions
SYSTEM_PROMPT = """
You are 'Fuchsia', the friendly and knowledgeable Health Concierge for Fuchsia Desserts (Founder: Tosan).
Introduce yourself warmly as 'Fuchsia'. Speak in a candid, encouraging, expert tone. Avoid heavy medical or technical jargon.

CORE PRINCIPLE:
Every single dessert product at Fuchsia Desserts connects to a real health and ingredient benefit!
- Dark Chocolate/Cocoa = Heart circulation, mood-boosting endorphins, and rich antioxidants.
- Berries & Fruits = Immune support, skin glow, vitamins, and natural digestion.
- Nuts & Seeds = Healthy fats, sustained physical energy, and brain focus.
- Low-Sugar/Keto/Gluten-Free = Balanced blood sugar, weight management, and digestive comfort.

Your Job:
1. Educate the user on the specific health benefits of the product OR health goal they selected in plain, friendly terms.
2. Recommend specific, delicious Fuchsia Desserts items that fit.
3. For events and gifts, curate tailored dessert packages, quantities, and presentation ideas while highlighting the wholesome health benefits.
"""

# 4 Clean, Concise Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🌿 Product Benefits", 
    "🎯 Goal Matcher", 
    "🎉 Event Planner", 
    "🎁 Luxury Gifts"
])

api_key = st.secrets.get("OPENAI_API_KEY", "")

# --- TAB 1: Product Benefits ---
with tab1:
    with st.form("product_form"):
        st.subheader("Discover Product Health Benefits")
        product_choice = st.selectbox(
            "Select a specific dessert to learn its health benefits:",
            [
                "Signature Dark Chocolate Cakes & Gateaux",
                "Artisanal Fresh Berry & Fruit Tarts",
                "Gourmet Parfaits & Layered Mousse Cups",
                "Nut & Seed Energy Bites & Protein Treats",
                "Low-Sugar & Keto-Friendly Dessert Box",
                "Gluten-Free & Dairy-Free Artisan Pastries"
            ]
        )
        submit_product = st.form_submit_button("Discover Health Benefits ✨")

    if submit_product:
        if not api_key:
            st.error("Please configure OPENAI_API_KEY in Streamlit secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Introduce yourself as Fuchsia, the Health Concierge. Educate the customer specifically on the wholesome health & ingredient benefits of Fuchsia Desserts' item: '{product_choice}'. Explain clearly how eating this treat supports their wellbeing in friendly, encouraging English."
            
            with st.spinner("Fuchsia is analyzing product benefits..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
                )
                st.success(f"Health Benefits of {product_choice}:")
                st.markdown(res.choices[0].message.content)

# --- TAB 2: Goal Matcher ---
with tab2:
    with st.form("goal_form"):
        st.subheader("Match Desserts to Your Health Goal")
        health_focus = st.selectbox(
            "Select your health goal to find matching desserts:",
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
        submit_goal = st.form_submit_button("Match Desserts to Goal ✨")

    if submit_goal:
        if not api_key:
            st.error("Please configure OPENAI_API_KEY in Streamlit secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Introduce yourself as Fuchsia, the Health Concierge. Recommend 2-3 delicious Fuchsia Desserts that match this specific health goal: '{health_focus}'. Explain clearly why these treats support that goal in warm, candid terms."
            
            with st.spinner("Fuchsia is matching desserts to your goal..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
                )
                st.success("Your Recommended Dessert Match:")
                st.markdown(res.choices[0].message.content)

# --- TAB 3: Event Planner ---
with tab3:
    with st.form("event_planner_form"):
        st.subheader("Plan Event & Party Catering")
        event_type = st.selectbox(
            "What type of event are you hosting?",
            [
                "Wedding Reception / Bridal Dessert Table",
                "Corporate Gala / Conference Catering",
                "Private Dinner Party / Intimate Gathering",
                "Birthday / Milestone Celebration"
            ]
        )
        guest_count = st.selectbox(
            "Estimated number of guests?",
            ["10 - 25 Guests (Intimate Gathering)", "26 - 50 Guests (Medium Party)", "51 - 100 Guests (Large Event)", "100+ Guests (Grand Event)"]
        )
        submit_event = st.form_submit_button("Plan My Event Menu 🎉")

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

# --- TAB 4: Luxury Gifts ---
with tab4:
    with st.form("luxury_gift_form"):
        st.subheader("Curate Luxury Dessert Gifts")
        gift_occasion = st.selectbox(
            "What is the gifting occasion?",
            [
                "Corporate Client / VIP Appreciation Box",
                "Birthday / Milestone Anniversary Gift",
                "Executive Thank You Hamper",
                "Get Well Soon / Mindful Wellness Gift"
            ]
        )
        gift_size = st.selectbox(
            "Select gift size preference:",
            ["Single Luxury Gift Box (1 - 2 People)", "Family / Small Team Gift Hamper (3 - 6 People)", "Bulk Executive Orders (Multiple Recipients)"]
        )
        submit_gift = st.form_submit_button("Curate Luxury Gift 🎁")

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
