import streamlit as st
import openai
import urllib.parse
from datetime import datetime

# Page Setup
st.set_page_config(
    page_title="Fuchsia Health Concierge | Fuchsia Desserts", 
    page_icon="🍰", 
    layout="centered"
)

# Custom High-End Styling (Signature Fuchsia Pink & Clean White Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Montserrat:wght@400;500;600;700;800&display=swap');

    /* 1. Page Background & Width */
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

    /* 5. TABS BAR */
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

    /* 6. SELECTBOX HARD OVERRIDE */
    [data-baseweb="select"],
    [data-baseweb="select"] > div,
    [data-baseweb="select"] [role="combobox"],
    [data-baseweb="select"] input {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }

    [data-baseweb="select"] *,
    [data-baseweb="select"] span,
    [data-baseweb="select"] div {
        color: #1A1A1A !important;
        -webkit-text-fill-color: #1A1A1A !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* 7. POPUP LIST OPTIONS */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 6px !important;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.08) !important;
    }

    ul[role="listbox"] li,
    li[role="option"] {
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
    }

    ul[role="listbox"] li:hover,
    li[role="option"]:hover,
    li[aria-selected="true"] {
        background-color: #FDF4FF !important;
        color: #D946EF !important;
        -webkit-text-fill-color: #D946EF !important;
    }

    /* 8. SIGNATURE FUCHSIA PINK BUTTON */
    button[kind="primaryFormSubmit"],
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

    /* 9. WHATSAPP CONCIERGE BUTTON */
    .fuchsia-wa-btn {
        display: block;
        text-align: center;
        background-color: #25D366;
        color: #FFFFFF !important;
        font-weight: 800;
        padding: 13px 18px;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 12px;
        text-transform: uppercase;
        font-size: 13px;
        letter-spacing: 0.5px;
        box-shadow: 0px 4px 12px rgba(37, 211, 102, 0.25);
    }
    .fuchsia-wa-btn:hover {
        background-color: #1EBE5D;
        color: #FFFFFF !important;
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

# --- TAB 1: Health Benefits ---
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
                answer_text = res.choices[0].message.content
                st.success(f"Health Benefits of {product_choice}:")
                st.markdown(answer_text)

                # WhatsApp Inquiry Dispatch
                wa_msg = f"🍰 *FUCHSIA DESSERTS HEALTH INQUIRY*\n━━━━━━━━━━━━━━━━━━━━\n🎯 *Product:* {product_choice}\n\n💡 *Concierge Notes:*\n{answer_text}\n\n━━━━━━━━━━━━━━━━━━━━\n✨ I would like to order or ask more about this treat!"
                wa_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(wa_msg)}"
                st.markdown(f'<a href="{wa_url}" target="_blank" class="fuchsia-wa-btn">📲 Order / Inquire via WhatsApp</a>', unsafe_allow_html=True)

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
                answer_text = res.choices[0].message.content
                st.success("Your Recommended Dessert Match:")
                st.markdown(answer_text)

                # WhatsApp Inquiry Dispatch
                wa_msg = f"🍰 *FUCHSIA DESSERTS HEALTH MATCH*\n━━━━━━━━━━━━━━━━━━━━\n🎯 *Health Goal:* {health_focus}\n\n💡 *Concierge Recommendation:*\n{answer_text}\n\n━━━━━━━━━━━━━━━━━━━━\n✨ I would like to order these recommended desserts!"
                wa_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(wa_msg)}"
                st.markdown(f'<a href="{wa_url}" target="_blank" class="fuchsia-wa-btn">📲 Order Matched Desserts via WhatsApp</a>', unsafe_allow_html=True)

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
                answer_text = res.choices[0].message.content
                st.success("Your Custom Event Catering Plan:")
                st.markdown(answer_text)

                # WhatsApp Catering Quote Dispatch
                wa_msg = f"🎉 *FUCHSIA DESSERTS EVENT CATERING QUOTE*\n━━━━━━━━━━━━━━━━━━━━\n🎪 *Event Type:* {event_type}\n👥 *Guest Count:* {guest_count}\n\n📋 *Curated Menu & Plan:*\n{answer_text}\n\n━━━━━━━━━━━━━━━━━━━━\n✨ Please provide pricing and availability for this date!"
                wa_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(wa_msg)}"
                st.markdown(f'<a href="{wa_url}" target="_blank" class="fuchsia-wa-btn">📲 Send Catering Request via WhatsApp</a>', unsafe_allow_html=True)

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
                answer_text = res.choices[0].message.content
                st.success("Your Curated Gift Package:")
                st.markdown(answer_text)

                # WhatsApp Gifting Dispatch
                wa_msg = f"🎁 *FUCHSIA DESSERTS LUXURY GIFT ORDER*\n━━━━━━━━━━━━━━━━━━━━\n🎀 *Occasion:* {gift_occasion}\n📦 *Box Size:* {gift_size}\n\n✨ *Curated Selection:*\n{answer_text}\n\n━━━━━━━━━━━━━━━━━━━━\n✨ Please confirm packaging options and delivery details!"
                wa_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(wa_msg)}"
                st.markdown(f'<a href="{wa_url}" target="_blank" class="fuchsia-wa-btn">📲 Order Luxury Gift Box via WhatsApp</a>', unsafe_allow_html=True)
