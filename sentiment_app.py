# ============================
# IMPORTS (VERY IMPORTANT)
# ============================
import streamlit as st
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ============================
# PAGE CONFIG
# ============================
st.set_page_config(
    page_title="Sentiment Analysis | Flipkart Reviews",
    page_icon="📊",
    layout="centered"
)

# ============================
# NLTK SAFE LOAD
# ============================
try:
    nltk.data.find("corpora/stopwords")
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("stopwords")
    nltk.download("wordnet")

# ============================
# LOAD MODEL & VECTORIZER
# ============================
@st.cache_resource
def load_model():
    model = joblib.load("sentiment_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_model()

# ============================
# TEXT PREPROCESSING
# ============================
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z]", " ", text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    words = [lemmatizer.lemmatize(w) for w in words]
    return " ".join(words)

# ============================
# FULL YELLOW BACKGROUND CSS
# ============================
st.markdown("""
<style>

/* FORCE FULL YELLOW BACKGROUND */
html, body, .stApp, .main, .block-container {
    background-color: #F9C74F !important;
}

/* REMOVE STREAMLIT DEFAULT DARK */
header, footer {
    background-color: #F9C74F !important;
}

/* WHITE CONTENT CARD */
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
    cursor: pointer;
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

# ============================
# UI LAYOUT
# ============================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

st.markdown(
    "<div class='title'>Sentiment Analysis of Real-time Flipkart Product Reviews</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Machine Learning & NLP powered review sentiment classification</div>",
    unsafe_allow_html=True
)

review = st.text_area(
    "Enter Flipkart Product Review",
    height=160,
    placeholder="Example: The product quality is excellent and delivery was fast."
)

analyze = st.button("Analyze Sentiment")

if analyze:
    if review.strip() == "":
        st.warning("Please enter a review.")
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
    "<div class='footer'>Built using Machine Learning, NLP & Streamlit | Internship Project</div>",
    unsafe_allow_html=True
)
