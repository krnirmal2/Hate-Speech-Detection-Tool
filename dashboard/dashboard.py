# Streamlit visualization dashboard
# dashboard/dashboard.py

# | Section            | Functionality                                |
# | ------------------ | -------------------------------------------- |
# | 📊 Bar Chart       | Number of users per risk level               |
# | 🔥 Top Influencers | Based on followers\_count                    |
# | 📝 Data Table      | Shows classified tweets and metadata         |
# | 🔄 Auto-refresh    | Refresh button to fetch live MongoDB updates |
# streamlit run dashboard/dashboard.py


import streamlit as st
import pandas as pd
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["jihadist_detection"]
collection = db["users"]

st.set_page_config(page_title="Jihadist Risk Dashboard", layout="wide")

st.title("🚨 Jihadist Detection Live Dashboard")
st.markdown("Monitors classified Twitter users based on NLP + graph-based clustering.")

# Refresh every 30 seconds
st_autorefresh = st.experimental_rerun if st.button("🔄 Refresh") else None

# Load data
data = pd.DataFrame(list(collection.find({}, {"_id": 0})))

if data.empty:
    st.warning("No data available in the database.")
    st.stop()

# Display total stats
st.subheader("📊 Risk Category Distribution")
risk_counts = data["risk_category"].value_counts()
st.bar_chart(risk_counts)

# Influential Users
st.subheader("🔥 Top Influential Users")
top_users = data.sort_values("followers_count", ascending=False).head(10)
st.table(top_users[["username", "followers_count", "risk_category"]])

# Display full records
st.subheader("📝 All Processed Tweets")
st.dataframe(data[["username", "text", "sentiment_score", "eigenvector_centrality", "risk_category"]])
