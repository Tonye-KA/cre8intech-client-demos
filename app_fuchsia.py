import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Fuchsia Health Concierge | Fuchsia Desserts", 
    page_icon="🍰", 
    layout="centered"
)

# Custom High-End Styling (Signature Fuchsia Pink, Pure White Canvas, White Dropdowns)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Montserrat:wght@400;500;600;700;800&display=swap');

    /* 1. Pure White Canvas & Container Width */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .main .block-container {
        padding-top: 2.5rem !important;
        max-width: 860px !important;
    }

    /* 2. Headings & Typography */
    h1, h2, h3, h4 {
        font-family: 'Playfair Display', serif !important;
        color: #1A1A1A !important;
        font-weight: 700 !important;
        line-height: 1.25 !important;
    }

    p, span, label, [data-testid="stMarkdownContainer"] p, [data-testid="stCaptionContainer"] p {
        color: #1E293B !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 500 !important;
    }

    /* Form Question Labels */
    label[data-testid="stWidgetLabel"] p {
        color: #1A1A1A !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }

    /* 3. Cre8intech Demo Badge */
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

    /* 4. Form Container Card */
    div[data-testid="stForm"], div.stBlock {
        background-color: #FAFAFA !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 14px !important;
        padding: 26px !important;
        box-shadow: 0px 4px 16px rgba(217, 70, 239, 0.05) !important;
        margin-top: 15px !important;
        margin-bottom: 20px !important;
    }

    /* 5. TABS BAR - COMPACT 1-LINE FIT & NO OVERFLOW */
    div[data-baseweb="tab-list"],
    div[data-testid="stTabs"] > div:first-child {
        border-bottom: 2px solid #F3E8FF !important;
        margin-bottom: 18px !important;
        display: flex !important;
        justify-content: space-between !important;
        width: 100% !important;
        gap: 4px !important;
        background: transparent !important;
    }

    [data-testid="stTabs"] button[aria-label="Scroll right"],
    [data-testid="stTabs"] button[aria-label="Scroll left"] {
        display: none !important;
    }

    button[data-baseweb="tab"],
    div[data-testid="stTabs"] button {
        padding: 8px 10px !important;
        margin: 0 !important;
        border-bottom: 2px solid transparent !important;
        white-space: nowrap !important;
    }

    button[data-baseweb="tab"] p,
    div[data-testid="stTabs"] button p {
        font-family: 'Playfair Display', serif !important;
        font-size: 13.5px !important;
        font-weight: 700 !important;
        color: #475569 !important;
    }

    button[aria-selected="true"] p,
    div[data-testid="stTabs"] button[aria-selected="true"] p {
        color: #D946EF !important;
    }

    /* 6. PERMANENT CRISP WHITE BACKGROUND ON THE DROPDOWN BOX */
    .stSelectbox,
    div[data-testid="stSelectbox"],
    div[data-testid="stSelectbox"] > div,
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] > div:first-child,
    div[data-baseweb="select"] [role="combobox"],
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] > div > div {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border-color: #E2E8F0 !important;
        border-radius: 8px !important;
    }

    /* Target inner text inside the closed dropdown */
    div[data-testid="stSelectbox"] *,
    div[data-baseweb="select"] *,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] [role="combobox"] * {
        color: #1A1A1A !important;
        -webkit-text-fill-color: #1A1A1A !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* Arrow icon inside dropdown */
    div[data-testid="stSelectbox"] svg,
    div[data-baseweb="select"] svg {
        fill: #64748B !important;
    }

    /* 7. DROPDOWN POPUP MENU */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"],
    div[role="listbox"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 6px !important;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.08) !important;
    }

    ul[role="listbox"] li,
    ul[role="listbox"] > li,
    li[role="option"],
    div[role="option"] {
        background-color: #FAF5FF !important;
        border: 1px solid #F3E8FF !important;
        border-radius: 6px !important;
        margin-bottom: 4px !important;
        color: #1E293B !important;
        -webkit-text-fill-color: #1E293B !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        padding: 10px 14px !important;
        opacity: 1 !important;
    }

    ul[role="listbox"] li *,
    li[role="option"] * {
        color: #1E293B !important;
        -webkit-text-fill-color: #1E293B !important;
        font-weight: 600 !important;
    }

    /* Hover & Selected Option State */
    ul[role="listbox"] li:hover,
    ul[role="listbox"] li:hover *,
    li[role="option"]:hover,
    li[role="option"]:hover *,
    li[aria-selected="true"],
    li[aria-selected="true"] * {
        background-color: #FDF4FF !important;
        color: #D946EF !important;
        -webkit-text-fill-color: #D946EF !important;
    }

    /* 8. SIGNATURE FUCHSIA PINK BUTTON + CRISP BOLD WHITE TEXT */
    button[kind="primaryFormSubmit"],
    button[kind="secondaryFormSubmit"],
    button[data-testid="baseButton-primary"],
    button[data-testid="baseButton-secondary"],
    div[data-testid="stFormSubmitButton"] button,
    div.stButton > button {
        background-color: #D946EF !important;
        background: #D946EF !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 13px 26px !important;
        margin-top: 14px !important;
        box-shadow: 0px 4px 14px rgba(217, 70, 239, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }

    button[kind="primaryFormSubmit"] *,
    button[kind="secondaryFormSubmit"] *,
    button[data-testid="baseButton-primary"] *,
    button[data-testid="baseButton-secondary"] *,
    div[data-testid="stFormSubmitButton"] button *,
    div.stButton > button * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 13px !important;
        font-weight: 800 !important;
        letter-spacing: 0.6px !important;
        text-transform: uppercase !important;
    }

    button[kind="primaryFormSubmit"]:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #C026D3 !important;
        background: #C026D3 !important;
        transform: translateY(-1px);
        box-shadow: 0px 6px 16px rgba(217, 70, 239, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<span class="demo-badge">CRE8INTECH PROTOTYPE DEMO</span>', unsafe_allow_html=True)
st.title("🍰 Fuchsia Health Concierge")
st.markdown("**Configured for Fuchsia Desserts** (Founder: Tosan)")
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

# 4 Balanced Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🌿 Health Benefits", 
    "🎯 Health Goal Matcher", 
    "🎉 Event Catering Planner", 
    "🎁 Luxury Gifts"
])

api_key = st.secrets.get("OPENAI_API_KEY", "")

# --- TAB 1: Health Benefits Finder ---
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
        submit_product = st.form_submit_button("Discover Health Benefits ✨", type="primary")

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

# --- TAB 2: Health Goal Matcher ---
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
        submit_goal = st.form_submit_button("Match Desserts to Goal ✨", type="primary")

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

# --- TAB 3: Event Catering Planner ---
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
        submit_event = st.form_submit_button("Plan My Event Menu 🎉", type="primary")

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

# --- TAB 4: Luxury Gifting Assistant ---
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
        submit_gift = st.form_submit_button("Curate Luxury Gift 🎁", type="primary")

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
