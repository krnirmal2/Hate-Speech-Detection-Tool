
# # Set up Twitter API credentials
# consumer_key = 'your_consumer_key'
# consumer_secret = 'your_consumer_secret'
# access_token = 'your_access_token'
# access_token_secret = 'your_access_token_secret'

# # Authenticate with the Twitter API
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth, wait_on_rate_limit=True)  # Set wait_on_rate_limit to avoid rate limiting issues

# # Define the target user you want to analyze
# target_user_screen_name = 'target_user'

# # Collect tweets and user data
# try:
#     target_user = api.get_user(screen_name=target_user_screen_name)
#     tweets = api.user_timeline(screen_name=target_user_screen_name, count=200, tweet_mode='extended')

#     # Print user information
#     print(f"User Name: {target_user.name}")
#     print(f"User Screen Name: {target_user.screen_name}")
#     print(f"User Followers Count: {target_user.followers_count}")
#     print(f"User Description: {target_user.description}\n")

#     # Print recent tweets
#     print("Recent Tweets:")
#     for i, tweet in enumerate(tweets, start=1):
#         print(f"Tweet {i}: {tweet.full_text}\n")

# except tweepy.TweepError as e:
#     print(f"Error: {e}")

    # 📄 Purpose:
    # Loads and preprocesses the dataset
    # Runs:
    # Sentiment analysis (BERT)
    # Graph creation & eigenvector centrality
    # Fuzzy clustering
    # Stores final classified results into MongoDB
    # Optionally visualizes results

from src.data_loader import load_data
from src.text_preprocessing import analyze_sentiment_bert
from src.graph_analysis import build_social_graph, compute_centrality_metrics
from src.fuzzy_clustering import perform_fuzzy_clustering, visualize_clusters
from src.database import save_users_to_db

import pandas as pd

# === Step 1: Load Data ===
print("📥 Loading dataset...")
df = load_data("data/tweets_1.csv")

# === Step 2: Sentiment Analysis ===
print("🧠 Performing sentiment analysis with BERT...")
df["sentiment_score"] = df["text"].apply(analyze_sentiment_bert)

# === Step 3: Build Graph & Compute Centrality ===
print("🔗 Building social graph...")
G = build_social_graph(df)
print("📊 Calculating eigenvector centrality...")
centrality_scores = compute_centrality_metrics(G)

# Add centrality to DataFrame
df["eigenvector_centrality"] = df["username"].map(centrality_scores).fillna(0)

# === Step 4: Clustering ===
print("🧪 Performing fuzzy clustering...")
df["followers_count"] = df["followers_count"].fillna(0)
cluster_labels, centers, fpc = perform_fuzzy_clustering(df)

# Map cluster index to readable risk categories
label_map = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
df["risk_category"] = [label_map.get(label, "Unknown") for label in cluster_labels]

# === Step 5: Store in MongoDB ===
print("💾 Saving classified users to MongoDB...")
records = df.to_dict(orient="records")
save_users_to_db(records)

# === Step 6: (Optional) Visualize ===
print("📈 Visualizing clusters...")
visualize_clusters(df, cluster_labels)

print("✅ Pipeline completed successfully.")