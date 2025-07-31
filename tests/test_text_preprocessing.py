import pytest
from src.text_preprocessing import (
    analyze_sentiment_bert,
    extract_keywords,
    calculate_engagement,
)
import pandas as pd


@pytest.fixture(scope="module")
def sentiment_model_fixture():
    # This fixture will load the model once for all tests in this module
    # No need to return anything, just ensure it loads without error
    # Mock the actual model loading to speed up tests
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.text_preprocessing.AutoTokenizer", lambda *args, **kwargs: MagicMock()
        )
        mp.setattr(
            "src.text_preprocessing.AutoModelForSequenceClassification",
            lambda *args, **kwargs: MagicMock(),
        )
        mp.setattr(
            "src.text_preprocessing.pipeline",
            lambda *args, **kwargs: MagicMock(
                return_value=[{"label": "LABEL_1", "score": 0.9}]
            ),
        )
        yield


def test_analyze_sentiment_bert_positive(sentiment_model_fixture):
    # Mock the actual sentiment analysis pipeline
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.text_preprocessing.sentiment_pipeline",
            MagicMock(return_value=[{"label": "LABEL_2", "score": 0.99}]),
        )
        sentiment_score = analyze_sentiment_bert("This is a wonderful day!")
        assert sentiment_score == 0.99


def test_analyze_sentiment_bert_negative(sentiment_model_fixture):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.text_preprocessing.sentiment_pipeline",
            MagicMock(return_value=[{"label": "LABEL_0", "score": 0.95}]),
        )
        sentiment_score = analyze_sentiment_bert("I hate this terrible situation.")
        assert (
            sentiment_score == 0.05
        )  # Assuming LABEL_0 is negative, score is 1-confidence


def test_analyze_sentiment_bert_neutral(sentiment_model_fixture):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.text_preprocessing.sentiment_pipeline",
            MagicMock(return_value=[{"label": "LABEL_1", "score": 0.8}]),
        )
        sentiment_score = analyze_sentiment_bert("The weather is calm.")
        assert sentiment_score == 0.5  # Assuming LABEL_1 is neutral, score is 0.5


def test_analyze_sentiment_bert_empty_text(sentiment_model_fixture):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.text_preprocessing.sentiment_pipeline",
            MagicMock(return_value=[{"label": "LABEL_1", "score": 0.5}]),
        )
        sentiment_score = analyze_sentiment_bert("")
        assert sentiment_score == 0.5  # Default for empty text


def test_extract_keywords():
    text = "This tweet is about hate speech and extremism. It contains keywords relevant to hate."
    keywords = extract_keywords(text)
    assert isinstance(keywords, list)
    assert "hate" in keywords
    assert "speech" in keywords
    assert "extremism" in keywords
    assert "keywords" in keywords


def test_extract_keywords_empty_text():
    keywords = extract_keywords("")
    assert keywords == []


def test_calculate_engagement():
    df = pd.DataFrame(
        {
            "retweet_count": [10, 20, 5, 0],
            "reply_count": [2, 4, 1, 0],
            "followers": [100, 200, 50, 10],
        }
    )
    df["engagement"] = calculate_engagement(df)

    # Expected calculations (simplified): (retweet_count + reply_count) / followers
    # row 0: (10 + 2) / 100 = 0.12
    # row 1: (20 + 4) / 200 = 0.12
    # row 2: (5 + 1) / 50 = 0.12
    # row 3: (0 + 0) / 10 = 0.0 (handle division by zero if followers is 0, here it's 10)

    assert df.loc[0, "engagement"] == pytest.approx(0.12)
    assert df.loc[1, "engagement"] == pytest.approx(0.12)
    assert df.loc[2, "engagement"] == pytest.approx(0.12)
    assert df.loc[3, "engagement"] == pytest.approx(0.0)


def test_calculate_engagement_zero_followers():
    df = pd.DataFrame({"retweet_count": [10], "reply_count": [2], "followers": [0]})
    df["engagement"] = calculate_engagement(df)
    assert df.loc[0, "engagement"] == 0.0  # Should be 0.0 to avoid division by zero
