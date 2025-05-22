# BERT-based sentiment analysis# src/text_preprocessing.py

from transformers import pipeline

# Load the BERT sentiment model once
bert_sentiment = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

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
        label = result[0]['label']

        # Convert star ratings to [-1, +1] scale
        star_map = {
            '1 star': -1.0,
            '2 stars': -0.5,
            '3 stars': 0.0,
            '4 stars': 0.5,
            '5 stars': 1.0
        }
        return star_map.get(label.lower(), 0.0)
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return 0.0
