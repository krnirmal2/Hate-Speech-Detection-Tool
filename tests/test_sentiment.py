import pytest
from src.text_preprocessing import analyze_sentiment


def test_sentiment_analysis():
    # Test positive sentiment
    positive_text = "I love this project! It's amazing and helpful."
    assert analyze_sentiment(positive_text) > 0

    # Test negative sentiment
    negative_text = "I hate this project! It's terrible and useless."
    assert analyze_sentiment(negative_text) < 0

    # Test neutral sentiment
    neutral_text = "This is a project about hate speech detection."
    sentiment = analyze_sentiment(neutral_text)
    assert -0.1 <= sentiment <= 0.1

    # Test empty text
    with pytest.raises(ValueError):
        analyze_sentiment("")

    # Test very long text
    long_text = "test " * 1000
    sentiment = analyze_sentiment(long_text)
    assert isinstance(sentiment, float)
    assert -1 <= sentiment <= 1
