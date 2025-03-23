import os
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from gtts import gTTS
from deep_translator import GoogleTranslator
from keybert import KeyBERT
import logging
from config import NEWS_API_KEY, MAX_ARTICLES, LOG_FILE
import sys
import os

# Ensure 'config/' folder is in the import path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from config import NEWS_API_KEY, MAX_ARTICLES, LOG_FILE

# Set up logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load NLP models at startup
nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()
kw_model = KeyBERT()
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")

# Fetch news articles
def fetch_news_links(company):
    """Fetches news articles from NewsAPI."""
    url = f"https://newsapi.org/v2/everything?q={company}&language=en&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get("status") == "error" or not data.get("articles"):
            return []
    except requests.exceptions.RequestException:
        return []

    return [
        {"Title": a["title"], "URL": a["url"], "Content": fetch_news_content(a["url"])}
        for a in data["articles"][:MAX_ARTICLES]
    ]

# Fetch actual article content
def fetch_news_content(url):
    """Fetches article text using BeautifulSoup."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return "Content could not be retrieved."
    except requests.exceptions.RequestException:
        return "Content not available."

    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    return " ".join([p.text for p in paragraphs[:10]]) or "Content unavailable."

# Summarization
def summarize_text(text):
    """Summarizes article content."""
    return summarizer(text[:1024], max_length=150, min_length=50, do_sample=False)[0]['summary_text']

# Sentiment Analysis
def analyze_sentiment(text):
    """Determines sentiment polarity."""
    score = sia.polarity_scores(text)
    return "Positive" if score['compound'] >= 0.05 else "Negative" if score['compound'] <= -0.05 else "Neutral"

# Extract Key Topics
def extract_topics(text):
    """Extracts topics using KeyBERT."""
    return [t[0] for t in kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')[:3]]

# Convert text to Hindi speech
def generate_hindi_tts(text, company):
    """Translates text to Hindi and converts to speech."""
    os.makedirs("static", exist_ok=True)
    translated_text = GoogleTranslator(source="auto", target="hi").translate(text)
    filename = f"static/{company.lower()}_news_summary.mp3"
    tts = gTTS(text=translated_text, lang='hi')
    tts.save(filename)
    return filename
