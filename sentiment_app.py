import streamlit as st
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ======================================================
# PAGE CONFIG (ONLY ONCE)
# ======================================================
st.set_page_config(
    page_title="Customer Sentiment Intelligence",
    page_icon="📊",
    layout="centered"
)

# ======================================================
# DOWNLOAD NLTK DATA (CACHED)
# ======================================================
@st.cache_resource
def load_nltk():
    nltk.download("stopwords")
    nltk.download("wordnet")

load_nltk()

# ======================================================
# LOAD MODEL & VECTORIZER (CACHED)
# ======================================================
@st.cache_resource
def load_model():
    model = joblib.load("sentiment_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_model()

# ======================================================
# TEXT PREPROCESSING
# ======================================================
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z]", " ", text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    words = [lemmatizer.lemmatize(w) for w in words]
    return " ".join(words)

# ======================================================
# CUSTOM CSS (UNIQUE DARK GLASS DESIGN)
# ======================================================
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f2027, #203a43, #2c5364);
}

.main {
    background: transparent;
}

.glass-card {
    max-width: 720px;
    margin: auto;
    margin-top: 40px;
    padding: 35px;
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(18px);
    box-shadow: 0 0 40px rgba(0, 255, 255, 0.15);
    border: 1px solid rgba(255,255,255,0.15);
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #00f2fe;
    letter-spacing: 1px;
}

.subtitle {
    text-align: center;
    font-size: 16px;
    color: #d1d5db;
    margin-bottom: 35px;
}

.stTextArea textarea {
    background: rgba(255,255,255,0.12);
    color: white;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.3);
    font-size: 15px;
}

.stButton button {
    width: 100%;
    border-radius: 14px;
    padding: 14px;
    font-size: 17px;
    font-weight: 600;
    background: linear-gradient(90deg, #00f2fe, #4facfe);
    color: #000;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0,242,254,0.5);
}

.result {
    margin-top: 25px;
    padding: 14px 28px;
    border-radius: 50px;
    text-align: center;
    font-size: 20px;
    font-weight: 700;
    display: inline-block;
}

.positive {
    background: linear-gradient(90deg, #00ff99, #00cc66);
    color: #003300;
}

.negative {
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    color: white;
}

.footer {
    text-align: center;
    margin-top: 45px;
    color: #9ca3af;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# UI LAYOUT
# ======================================================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

st.markdown(
    "<div class='title'>Customer Sentiment Intelligence</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>AI-powered sentiment classification for e-commerce reviews</div>",
    unsafe_allow_html=True
)

review = st.text_area(
    "Enter customer review",
    height=150,
    placeholder="Example: The product quality is excellent and delivery was fast."
)

analyze = st.button("Analyze Sentiment")

if analyze:
    if review.strip() == "":
        st.warning("Please enter a review to analyze.")
    else:
        with st.spinner("Analyzing sentiment..."):
            cleaned_text = clean_text(review)
            vectorized_text = vectorizer.transform([cleaned_text])
            prediction = model.predict(vectorized_text)[0]

        if prediction == 1:
            st.markdown(
                "<div style='text-align:center'><span class='result positive'>POSITIVE SENTIMENT</span></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div style='text-align:center'><span class='result negative'>NEGATIVE SENTIMENT</span></div>",
                unsafe_allow_html=True
            )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='footer'>Built with Machine Learning & Streamlit</div>",
    unsafe_allow_html=True
)
