# Custom Brand Styling (Green Obsidian Palette - Fixed Text Contrast)
st.markdown("""
    <style>
    /* Force main app background */
    .stApp {
        background-color: #F0FDF4 !important;
        color: #0F382C !important;
    }
    
    /* Title and Subtitles */
    h1, h2, h3, p, span, label {
        color: #0F382C !important;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Fix Chat Message Text Visibility */
    [data-testid="stChatMessageContent"] {
        background-color: #FFFFFF !important;
        color: #0F382C !important;
        border-radius: 10px;
        padding: 12px;
        border: 1px solid #10B981;
    }
    
    [data-testid="stChatMessageContent"] p, 
    [data-testid="stChatMessageContent"] li, 
    [data-testid="stChatMessageContent"] div {
        color: #0F382C !important;
        font-weight: 500;
    }

    /* Buttons */
    .stButton>button {
        background-color: #0F382C !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: none;
        padding: 10px 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #10B981 !important;
        color: #FFFFFF !important;
    }

    /* Demo Badge */
    .demo-badge {
        background-color: #10B981;
        color: white !important;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)
