from prometheus_client import Counter, Histogram, Gauge
from functools import wraps
import time

# Metrics
TWEETS_PROCESSED = Counter("tweets_processed_total", "Total number of tweets processed")

TWEETS_BY_RISK = Counter(
    "tweets_by_risk_total", "Number of tweets by risk level", ["risk_level"]
)

PROCESSING_TIME = Histogram("tweet_processing_seconds", "Time spent processing tweets")

SENTIMENT_SCORE = Gauge("tweet_sentiment_score", "Sentiment score of processed tweets")

CENTRALITY_SCORE = Gauge(
    "user_centrality_score", "Centrality score of users", ["username"]
)


def track_processing_time(func):
    """Decorator to track processing time of functions."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        PROCESSING_TIME.observe(time.time() - start_time)
        return result

    return wrapper


def update_metrics(tweet_data: dict):
    """Update Prometheus metrics with tweet data."""
    TWEETS_PROCESSED.inc()

    # Update risk level counter
    risk_level = ["Low", "Medium", "High"][tweet_data.get("cluster", 0)]
    TWEETS_BY_RISK.labels(risk_level=risk_level).inc()

    # Update sentiment score
    SENTIMENT_SCORE.set(tweet_data.get("sentiment_score", 0))

    # Update centrality score
    CENTRALITY_SCORE.labels(username=tweet_data.get("username", "unknown")).set(
        tweet_data.get("centrality_score", 0)
    )
