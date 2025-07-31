from datetime import datetime, timedelta

from config import MONGODB_DB, MONGODB_URI
from database import get_mongo_client
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Page config
st.set_page_config(
    page_title="Hate Speech Detection Dashboard", page_icon="🚨", layout="wide"
)

# Title
st.title("🚨 Hate Speech Detection Dashboard")

# MongoDB connection
db = get_mongo_client(MONGODB_URI)[MONGODB_DB]

# Sidebar filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Date Range", value=(datetime.now() - timedelta(days=7), datetime.now())
)

risk_level = st.sidebar.multiselect(
    "Risk Level", options=["Low", "Medium", "High"], default=["High"]
)


# Helper functions
def get_risk_label(cluster):
    return ["Low", "Medium", "High"][cluster]


def load_data():
    """Load data from MongoDB based on filters."""
    query = {
        "timestamp": {
            "$gte": date_range[0].isoformat(),
            "$lte": date_range[1].isoformat(),
        }
    }

    if risk_level:
        cluster_map = {"Low": 0, "Medium": 1, "High": 2}
        query["cluster"] = {"$in": [cluster_map[r] for r in risk_level]}

    data = list(db.tweets.find(query))
    return pd.DataFrame(data)


# Main content
try:
    df = load_data()

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Tweets", len(df))

    with col2:
        high_risk = len(df[df["cluster"] == 2])
        st.metric("High Risk Tweets", high_risk)

    with col3:
        avg_sentiment = df["sentiment_score"].mean()
        st.metric("Average Sentiment", f"{avg_sentiment:.2f}")

    with col4:
        unique_users = df["username"].nunique()
        st.metric("Unique Users", unique_users)

    # Sentiment Distribution
    st.subheader("Sentiment Distribution")
    fig_sentiment = px.histogram(
        df,
        x="sentiment_score",
        color="cluster",
        color_discrete_sequence=["green", "orange", "red"],
        labels={"sentiment_score": "Sentiment Score", "cluster": "Risk Level"},
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)

    # Risk Level Distribution
    st.subheader("Risk Level Distribution")
    risk_counts = df["cluster"].value_counts().sort_index()
    fig_risk = px.pie(
        values=risk_counts.values,
        names=[get_risk_label(i) for i in risk_counts.index],
        color_discrete_sequence=["green", "orange", "red"],
    )
    st.plotly_chart(fig_risk, use_container_width=True)

    # Top Users by Centrality
    st.subheader("Top Users by Influence")
    top_users = df.nlargest(10, "centrality_score")
    fig_users = px.bar(
        top_users,
        x="username",
        y="centrality_score",
        color="cluster",
        color_discrete_sequence=["green", "orange", "red"],
        labels={"centrality_score": "Influence Score", "username": "Username"},
    )
    st.plotly_chart(fig_users, use_container_width=True)

    # Recent High-Risk Tweets
    st.subheader("Recent High-Risk Tweets")
    high_risk_tweets = df[df["cluster"] == 2].sort_values("timestamp", ascending=False)
    for _, tweet in high_risk_tweets.head(5).iterrows():
        st.markdown(
            f"""
        **{tweet['username']}** ({tweet['timestamp']})
        > {tweet['text']}
        - Sentiment: {tweet['sentiment_score']:.2f}
        - Influence: {tweet['centrality_score']:.2f}
        ---
        """
        )

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please check your MongoDB connection and filters.")
