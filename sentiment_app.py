import streamlit as st
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Sentiment Analysis | Flipkart Reviews",
    page_icon="📊",
    layout="centered"
)

# =====================================================
# NLTK SAFE LOADING (NO HANGING)
# =====================================================
try:
    nltk.data.find("corpora/stopwords")
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("stopwords")
    nltk.download("wordnet")

# =====================================================
# LOAD MODEL & VECTORIZER
# =====================================================
@st.cache_resource
def load_model():
    model = joblib.load("sentiment_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_model()

# =====================================================
# TEXT PREPROCESSING
# =====================================================
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z]", " ", text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    words = [lemmatizer.lemmatize(w) for w in words]
    return " ".join(words)

# =====================================================
# CUSTOM UI THEME (MIDNIGHT BLUE + TEAL)
# =====================================================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

.glass-card {
    background: rgba(15, 23, 42, 0.95);
    padding: 35px;
    border-radius: 22px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.7);
    border: 1px solid rgba(34, 211, 238, 0.2);
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: 800;
    background: linear-gradient(90deg, #22d3ee, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    font-size: 16px;
    color: #cbd5e1;
    margin-bottom: 30px;
}

.stTextArea textarea {
    background: #020617;
    color: white;
    border-radius: 14px;
    border: 1px solid #22d3ee;
    font-size: 15px;
}

.stButton button {
    width: 100%;
    border-radius: 14px;
    padding: 14px;
    font-size: 18px;
    font-weight: 600;
    background: linear-gradient(90deg, #22d3ee, #06b6d4);
    color: #020617;
    border: none;
    transition: 0.3s;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(34,211,238,0.5);
}

.result {
    margin-top: 25px;
    padding: 16px 30px;
    border-radius: 50px;
    font-size: 22px;
    font-weight: 700;
    text-align: center;
    display: inline-block;
}

.positive {
    background: linear-gradient(90deg, #22c55e, #4ade80);
    color: #022c22;
}

.negative {
    background: linear-gradient(90deg, #ef4444, #f87171);
    color: #450a0a;
}

.footer {
    text-align: center;
    margin-top: 40px;
    font-size: 13px;
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# UI LAYOUT
# =====================================================
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
    "<div class='footer'>Built using Machine Learning, NLP & Streamlit | Internship Project</div>",
    unsafe_allow_html=True
)
