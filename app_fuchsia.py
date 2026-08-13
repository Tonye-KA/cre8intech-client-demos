import streamlit as st
import openai

# Page Setup
st.set_page_config(
    page_title="Fuchsia AI Concierge | Fuchsia Desserts", 
    page_icon="🍰", 
    layout="centered"
)

# Custom High-End Styling (Fuchsia Desserts Minimalist Luxury Palette)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Montserrat:wght@400;500;600;700&display=swap');

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
        background-color: #D946EF !important;
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

    div[data-testid="stForm"], div.stBlock {
        background-color: #FAFAFA !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 28px !important;
        box-shadow: 0px 4px 20px rgba(217, 70, 239, 0.05) !important;
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

    div.stButton > button {
        background-color: #D946EF !important;
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
st.write("Welcome! Learn about the **health benefits** of our products or plan custom **event dessert catering & luxury gifts**.")

# System Prompt
SYSTEM_PROMPT = """
You are the 'Fuchsia AI Concierge' for Fuchsia Desserts (Founder: Tosan).
Your role is to:
1. Educate customers on the specific HEALTH BENEFITS of ingredients used in Fuchsia Desserts (antioxidants in dark cocoa, natural fruit nutrients, low-glycemic natural sweeteners, fiber in nuts/seeds, gut-friendly options).
2. Recommend specific products based on the health benefit or dietary goal they selected.
3. Assist with Event Catering (weddings, corporate galas, private dining) and Luxury Gifts by suggesting tailored dessert menus, platter quantities, and presentation ideas.

Be elegant, warm, educational, and professional. Use structured bullet points.
"""

# Tabs
tab1, tab2, tab3 = st.tabs(["🌿 Health Benefits & Product Matcher", "🎉 Event Catering Planner", "🎁 Luxury Gift Assistant"])

api_key = st.secrets.get("OPENAI_API_KEY", "")

# --- TAB 1: Health Benefits & Product Matcher ---
with tab1:
    with st.form("health_form"):
        st.subheader("Discover Product Health Benefits")
        
        health_focus = st.selectbox(
            "1. What health benefit or dietary goal are you looking for?",
            [
                "Antioxidants & Cardiovascular Health (Dark Chocolate/Berries)",
                "Energy Boost & Sustained Vitality (Nuts, Seeds & Superfoods)",
                "Low Sugar / Glycemic-Friendly (Diabetic & Weight-Conscious)",
                "Gluten-Free & Easy Digestion",
                "Keto / Low-Carb High-Healthy-Fats",
                "Pure Clean Ingredients (No Artificial Additives)"
            ]
        )
        
        product_interest = st.selectbox(
            "2. What type of dessert are you considering?",
            ["Signature Cakes & Parfaits", "Artisanal Tarts & Pastries", "Dessert Shots & Mini Bites", "Custom Gourmet Box", "Surprise Me Based on Health Benefit"]
        )
        
        submit_health = st.form_submit_button("Explain Health Benefits & Recommend Product 🌿")

    if submit_health:
        if not api_key:
            st.error("Please configure OPENAI_API_KEY in Streamlit secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Educate the customer on the specific health benefits of Fuchsia Desserts' products for: Health Focus = {health_focus}, Product Interest = {product_interest}. Provide 2-3 specific product recommendations and detail why the ingredients are beneficial for their health."
            
            with st.spinner("Analyzing ingredient health benefits..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
                )
                st.success("Health Benefits & Product Breakdown:")
                st.markdown(res.choices[0].message.content)

# --- TAB 2: Event Catering Planner ---
with tab2:
    with st.form("event_form"):
        st.subheader("Event & Party Dessert Catering")
        
        event_type = st.selectbox(
            "1. What type of event are you hosting?",
            [
                "Wedding / Reception Dessert Table",
                "Corporate Gala / Conference Catering",
                "Bridal Shower / Baby Shower",
                "Private Dinner Party",
                "Birthday / Anniversary Celebration"
            ]
        )
        
        guest_count = st.selectbox(
            "2. Estimated number of guests?",
            ["10 - 25 Guests (Intimate Gathering)", "26 - 50 Guests (Medium Party)", "51 - 100 Guests (Large Event)", "100+ Guests (Grand Event)"]
        )
        
        event_style = st.selectbox(
            "3. Preferred dessert presentation style?",
            ["Individual Plated Desserts", "Interactive Dessert Station / Buffet", "Mini Dessert Shots & Finger Foods", "Assorted Grazing Platter"]
        )
        
        submit_event = st.form_submit_button("Plan My Event Dessert Menu 🎉")

    if submit_event:
        if not api_key:
            st.error("Please configure OPENAI_API_KEY in Streamlit secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Create an event dessert catering proposal for Fuchsia Desserts: Event Type = {event_type}, Guest Count = {guest_count}, Presentation Style = {event_style}. Detail estimated quantities, variety mix, presentation tips, and highlight healthy options included."
            
            with st.spinner("Curating your event dessert catering plan..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
                )
                st.success("Your Event Catering Plan:")
                st.markdown(res.choices[0].message.content)

# --- TAB 3: Luxury Gift Assistant ---
with tab3:
    with st.form("gift_form"):
        st.subheader("Curated Luxury Gifting")
        
        gift_occasion = st.selectbox(
            "1. What is the gifting occasion?",
            ["Corporate Client Appreciation", "Executive / VIP Gift Box", "Birthday / Milestone Gift", "Romantic / Anniversary Gift", "Get Well Soon / Mindful Gift"]
        )
        
        packaging_pref = st.selectbox(
            "2. Gifting style preference?",
            ["Bespoke Ribboned Gift Box", "Luxury Dessert Hamper", "Personalized Individual Treat Box", "Custom Branded Corporate Box"]
        )
        
        submit_gift = st.form_submit_button("Curate Gift Package 🎁")

    if submit_gift:
        if not api_key:
            st.error("Please configure OPENAI_API_KEY in Streamlit secrets.")
        else:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Curate a luxury dessert gift box for Fuchsia Desserts: Occasion = {gift_occasion}, Packaging Style = {packaging_pref}. Include product selection, packaging details, and note the health/wholesome qualities of the gift."
            
            with st.spinner("Curating your luxury gift box..."):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
                )
                st.success("Your Curated Gift Package:")
                st.markdown(res.choices[0].message.content)
