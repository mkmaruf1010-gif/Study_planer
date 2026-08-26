# Custom Dark Theme Styling (with high-contrast dropdown text & labels)
st.markdown("""
    <style>
    /* Main Background & Base Text */
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 25px;
        color: #00E5FF;
        text-shadow: 0 0 10px rgba(0,229,255,0.3);
    }

    /* Fix Dropdown / Selectbox Labels Visibility */
    .stSelectbox label {
        color: #00E5FF !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* Fix Dropdown Input Box & Text */
    div[data-baseweb="select"] > div {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
    }

    /* Fix Dropdown Selected Value Text */
    div[data-baseweb="select"] span {
        color: #FFFFFF !important;
    }

    /* Metrics Styling */
    .metric-container {
        text-align: center;
        padding: 15px;
        background-color: #1E1E1E;
        border-radius: 10px;
        border: 1px solid #333333;
    }
    .metric-label {
        font-size: 13px;
        letter-spacing: 0.5px;
        color: #A0A0A0;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #00E5FF;
        margin-top: 5px;
    }
    .divider {
        border-right: 1px solid #333333;
        height: 50px;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)
