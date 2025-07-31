# Streamlit visualization dashboard
# dashboard/dashboard.py

# | Section            | Functionality                                |
# | ------------------ | -------------------------------------------- |
# | 📊 Bar Chart       | Number of users per risk level               |
# | 🔥 Top Influencers | Based on followers\_count                    |
# | 📝 Data Table      | Shows classified tweets and metadata         |
# | 🔄 Auto-refresh    | Refresh button to fetch live MongoDB updates |
# streamlit run dashboard/dashboard.py


import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

import streamlit as st
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

from src.config.config import MONGODB_URI, MONGODB_DB
from src.repository.database import get_mongo_client

# 📌 Streamlit dashboard setup
# Sets the page layout and title.
st.set_page_config(page_title="Jihadist Risk Dashboard", layout="wide")
st.title("🚨 Jihadist Detection Live Dashboard")
st.markdown("Monitors classified Twitter users based on NLP + graph-based clustering.")

# MongoDB connection
st.write(f"Using MongoDB URI: {MONGODB_URI}")
st.write(f"Using Database: {MONGODB_DB}")

try:
    client = get_mongo_client()
    db = client["local"]
    collection = db["hate_speech_detection"]
    count = collection.count_documents({})
    st.write(f"Number of documents in hate_speech_detection: {count}")
    st.success("Connected to MongoDB successfully.")
except Exception as e:
    st.error(f"Failed to connect to MongoDB: {str(e)}")
    st.stop()

# 🔄 Refresh Button
# Allows users to manually refresh the dashboard to get the latest data from MongoDB.
st_autorefresh = st.experimental_rerun if st.button("🔄 Refresh") else None

# 📌 Data loading from MongoDB
# Fetches all records from the "users" collection and converts them to a Pandas DataFrame.
data = pd.DataFrame(list(collection.find({}, {"_id": 0})))
st.write(f"Number of records fetched: {len(data)}")

# ❌ No data fallback
# Stops the dashboard gracefully if no data is available.
if data.empty:
    st.warning("No data available in the database.")
    st.stop()

# 📊 Risk Distribution Bar Chart
# Visualizes how many users fall into each risk category.
st.subheader("📊 Risk Category Distribution")
risk_counts = data["risk_category"].value_counts()
st.bar_chart(risk_counts)

# 🔥 Top Influential Users
# Displays the top 10 users sorted by follower count to identify high-impact accounts.
st.subheader("🔥 Top Influential Users")
top_users = data.sort_values("followers", ascending=False).head(10)
st.table(top_users[["username", "followers", "risk_category"]])

# 📝 Detailed Tweet and Metadata Table
# Shows detailed information for all classified users including sentiment and centrality metrics.
st.subheader("📝 All Processed Tweets")
st.dataframe(
    data[
        [
            "username",
            "tweets",
            "sentiment_score",
            "eigenvector_centrality",
            "risk_category",
        ]
    ]
)
