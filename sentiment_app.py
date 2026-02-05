st.markdown("""
<style>

/* FORCE FULL YELLOW BACKGROUND — NO DARK ANYWHERE */
html, body {
    background-color: #F9C74F !important;
}

.stApp {
    background-color: #F9C74F !important;
}

.main {
    background-color: #F9C74F !important;
}

.block-container {
    background-color: #F9C74F !important;
}

/* REMOVE DEFAULT STREAMLIT PADDING SHADOW */
section[data-testid="stSidebar"] {
    background-color: #F9C74F !important;
}

/* MAIN WHITE CARD */
.glass-card {
    background-color: #FFFFFF;
    padding: 42px;
    border-radius: 24px;
    max-width: 900px;
    margin: 60px auto;
    box-shadow: 0 20px 40px rgba(0,0,0,0.12);
}

/* TITLE */
.title {
    text-align: center;
    font-size: 40px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 10px;
}

/* SUBTITLE */
.subtitle {
    text-align: center;
    font-size: 15px;
    color: #374151;
    margin-bottom: 36px;
}

/* TEXT AREA */
.stTextArea textarea {
    background-color: #FFF7ED;
    color: #111827;
    border-radius: 16px;
    border: 1px solid #F8961E;
    font-size: 15px;
}

/* ORANGE CTA BUTTON */
.stButton button {
    width: 100%;
    border-radius: 16px;
    padding: 14px;
    font-size: 17px;
    font-weight: 600;
    background-color: #F8961E;
    color: #111827;
    border: none;
    box-shadow: 0 8px 18px rgba(248,150,30,0.35);
}

.stButton button:hover {
    background-color: #F3722C;
    color: #FFFFFF;
}

/* RESULT BADGE */
.result {
    margin-top: 32px;
    padding: 14px 36px;
    border-radius: 50px;
    font-size: 20px;
    font-weight: 700;
    display: inline-block;
}

/* SENTIMENT COLORS */
.positive {
    background-color: #22C55E;
    color: #FFFFFF;
}

.negative {
    background-color: #EF4444;
    color: #FFFFFF;
}

/* FOOTER */
.footer {
    text-align: center;
    margin-top: 50px;
    font-size: 13px;
    color: #374151;
}

</style>
""", unsafe_allow_html=True)
