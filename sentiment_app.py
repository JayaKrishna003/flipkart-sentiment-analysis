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
# SAFE NLTK LOAD
# =====================================================
try:
    nltk.data.find("corpora/stopwords")
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("stopwords")
    nltk.download("wordnet")

# =====================================================
# LOAD MODEL
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
# YELLOW–ORANGE PROFESSIONAL UI THEME
# =====================================================
st.markdown("""
<style>
body {
    background: #F9C74F;
    color: #1F2937;
}

/* Main Card */
.glass-card {
    background: #FFFFFF;
    padding: 40px;
    border-radius: 22px;
    max-width: 860px;
    margin: auto;
    box-shadow: 0 25px 50px rgba(0,0,0,0.15);
}

/* Title */
.title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #1F2937;
    margin-bottom: 8px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 15px;
    color: #374151;
    margin-bottom: 34px;
}

/* Label */
label {
    font-weight: 600;
}

/* Text Area */
.stTextArea textarea {
    background: #FFF7ED;
    color: #1F2937;
    border-radius: 14px;
    border: 1px solid #F8961E;
    font-size: 15px;
}

/* Button */
.stButton button {
    width: 100%;
    border-radius: 14px;
    padding: 14px;
    font-size: 17px;
    font-weight: 600;
    background: #F8961E;
    color: #1F2937;
    border: none;
}

.stButton button:hover {
    background: #F3722C;
    color: white;
}

/* Result */
.result {
    margin-top: 30px;
    padding: 14px 34px;
    border-radius: 40px;
    font-size: 20px;
    font-weight: 700;
    display: inline-block;
}

/* Positive / Negative */
.positive {
    background: #22C55E;
    color: white;
}

.negative {
    background: #EF4444;
    color: white;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 45px;
    font-size: 13px;
    color: #374151;
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
        st.warning("Please enter a review.")
    else:
        with st.spinner("Analyzing sentiment..."):
            cleaned = clean_text(review)
            vec = vectorizer.transform([cleaned])
            prediction = model.predict(vec)[0]

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
