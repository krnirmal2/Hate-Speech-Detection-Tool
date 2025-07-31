# BERT-based sentiment analysis# src/text_preprocessing.py

from transformers import pipeline
import re
from langdetect import detect
import spacy

# Load the BERT sentiment model once
bert_sentiment = pipeline(
    "sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment"
)

# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import os

    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def analyze_sentiment_bert(text: str) -> float:
    """
    Analyzes sentiment of text using BERT and returns a score.

    Args:
        text (str): Input tweet

    Returns:
        float: Compound sentiment score from -1 (negative) to +1 (positive)
    """
    try:
        result = bert_sentiment(text[:512])  # Limit to 512 tokens
        label = result[0]["label"]

        # Convert star ratings to [-1, +1] scale
        star_map = {
            "1 star": -1.0,
            "2 stars": -0.5,
            "3 stars": 0.0,
            "4 stars": 0.5,
            "5 stars": 1.0,
        }
        return star_map.get(label.lower(), 0.0)
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return 0.0


def preprocess_text(text: str):
    """
    Cleans, detects language, and lemmatizes the input text.
    Returns a dict with cleaned, language, and lemmatized text.
    """
    # Remove URLs, mentions, hashtags, emojis, non-ASCII
    cleaned = re.sub(r"http\S+|www\S+|@\w+|#\w+|[^\x00-\x7F]+", "", text)
    try:
        language = detect(cleaned)
    except Exception:
        language = "unknown"
    lemmatized = " ".join([token.lemma_ for token in nlp(cleaned)])
    return {"cleaned": cleaned, "language": language, "lemmatized": lemmatized}


JIHADISM_KEYWORDS = [
    "caliphate",
    "martyrdom",
    "jihad",
    "sharia",
    "infidel",
    "kafir",
    "mujahid",
    "takfir",
    "hijra",
    "shaheed",
]


def keyword_frequency(text: str, keywords=JIHADISM_KEYWORDS) -> int:
    """
    Counts the number of jihadism-related keywords in the text.
    """
    text_lower = text.lower()
    return sum(text_lower.count(word) for word in keywords)


def engagement_metric(row) -> float:
    """
    Computes engagement as (retweets + replies) / followers.
    Expects row to have 'retweet_count', 'reply_count', 'followers'.
    """
    followers = row.get("followers", 1) or 1  # Avoid division by zero
    return (row.get("retweet_count", 0) + row.get("reply_count", 0)) / followers
