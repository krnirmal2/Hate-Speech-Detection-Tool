# FastAPI endpoints
# 📄 Purpose:
# Provides REST endpoints for external tools or law enforcement
# Calls MongoDB module and NLP + clustering in real-time
# src/api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from src.database import get_users_by_risk
from src.text_preprocessing import analyze_sentiment_bert
from src.fuzzy_clustering import perform_fuzzy_clustering
from src.graph_analysis import compute_centrality_metrics, build_social_graph
import pandas as pd
import uvicorn

app = FastAPI(title="Jihadist Risk Classifier API", version="1.0")

# Mock user base to simulate influence score (used for real-time clustering)
mock_data = pd.DataFrame([
    {"username": "baseline_user", "text": "neutral tweet", "followers_count": 50,
     "sentiment_score": 0.0, "eigenvector_centrality": 0.1}
])

# Request Model
class TweetInput(BaseModel):
    username: str
    text: str
    followers_count: int


@app.get("/users/{risk_category}", response_model=List[dict])
def get_users(risk_category: str):
    """
    Returns users by risk category: High Risk, Medium Risk, Low Risk
    """
    try:
        users = get_users_by_risk(risk_category)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB Error: {e}")


@app.post("/analyze_tweet")
def classify_tweet(tweet: TweetInput):
    """
    Classifies a tweet and returns its predicted risk category.
    """
    try:
        # Step 1: Preprocess sentiment
        sentiment = analyze_sentiment_bert(tweet.text)

        # Step 2: Simulate influence score (real case would use graph)
        influence_score = 0.5  # Placeholder (could be from dynamic NetworkX update)

        # Step 3: Prepare data for clustering
        input_df = pd.DataFrame([{
            "sentiment_score": sentiment,
            "eigenvector_centrality": influence_score,
            "followers_count": tweet.followers_count
        }])

        cluster, _, _ = perform_fuzzy_clustering(input_df, num_clusters=3)

        label_map = {
            0: "Low Risk",
            1: "Medium Risk",
            2: "High Risk"
        }
        predicted_risk = label_map.get(cluster[0], "Unknown")

        return {
            "username": tweet.username,
            "risk_category": predicted_risk,
            "sentiment_score": sentiment,
            "followers_count": tweet.followers_count
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Processing Error: {e}")


# Uncomment if running standalone
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# | Endpoint              | Description                          |
# | --------------------- | ------------------------------------ |
# | `GET /users/{risk}`   | Fetch from MongoDB by risk level     |
# | `POST /analyze_tweet` | Real-time NLP + fuzzy classification |

# {
#   "username": "user123",
#   "text": "Death to infidels #jihad",
#   "followers_count": 1000
# }



