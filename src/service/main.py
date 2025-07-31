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
# 1.Loads and preprocesses the dataset
# Runs:
# 2.Sentiment analysis (BERT)
# 3.Graph creation & eigenvector centrality
# 4.Fuzzy clustering
# 5.Stores final classified results into MongoDB
# 6.Optionally visualizes results

import time
from pathlib import Path
from src.service.data_loader import load_data
from src.service.text_preprocessing import (
    analyze_sentiment_bert,
    keyword_frequency,
    engagement_metric,
)
from src.service.graph_analysis import (
    build_social_graph,
    compute_centrality_metrics,
    compute_all_centrality_metrics,
)
from src.service.clusteringStrategy.fuzzy_clustering import (
    perform_fuzzy_clustering,
    visualize_clusters,
    multi_run_fuzzy_clustering,
    fuzzy_silhouette_score,
    gustafson_kessel_clustering,
)
from src.repository.database import save_users_to_db
import pandas as pd
import numpy as np

print("**********************  STEPS TO BE FOLLOWED   ***************************")
print("1. 🔍 Loading dataset...")
print("2. 🧠 Performing sentiment analysis with BERT...")
print("3. 🔗 Building social graph...")
print("4. 📊 Calculating centrality metrics...")
print("5. 🧪 Performing clustering using strategy:  ...")
print("6.   Fuzzy Silhouette Score ")
print("7. 💾 Saving classified users to MongoDB...")
print("8. 📈 Visualizing clusters...")
print("9. ✅ Pipeline completed successfully.")

print(" ***********************  PROCESSING STARTED...**************************")
# === Step 1: Load Data ===
start_time = time.time()
print("1.🔍 Loading dataset...")
csv_path = Path("src") / "data" / "test.csv"
df = load_data(str(csv_path))
# df = load_data(r"E:\cursorAi\PYTHON\Hate-Speech-Detection-Tool\data\tweets_1.csv")
end_time = time.time()
print(f"   Time taken for Data Loading: {end_time - start_time:.2f} seconds.\n")

# === Step 2: Sentiment Analysis ===
start_time = time.time()
print("2.🧠 Performing sentiment analysis with BERT...")
df["sentiment_score"] = df["tweets"].apply(analyze_sentiment_bert)
end_time = time.time()
print(f"   Time taken for Sentiment Analysis: {end_time - start_time:.2f} seconds.\n")

# === Step 3: Build Graph & Compute Centrality ===
start_time = time.time()
print("3.🔗 Building social graph...")
G = build_social_graph(df)
print("4.📊 Calculating centrality metrics...")
all_centrality_scores = compute_all_centrality_metrics(G)

# Add all centralities to DataFrame
for metric in [
    "eigenvector_centrality",
    "closeness_centrality",
    "betweenness_centrality",
]:
    df[metric] = (
        df["username"]
        .map(lambda u: all_centrality_scores.get(u, {}).get(metric, 0))
        .fillna(0)
    )

# === Step 3.5: Add keyword frequency and engagement metrics ===
df["keyword_freq"] = df["tweets"].apply(keyword_frequency)
# Ensure retweet_count, reply_count columns exist (fillna 0 if missing)
if "retweet_count" not in df.columns:
    df["retweet_count"] = 0
if "reply_count" not in df.columns:
    df["reply_count"] = 0
df["engagement"] = df.apply(engagement_metric, axis=1)
end_time = time.time()
print(
    f"   Time taken for Graph Analysis and Feature Engineering: {end_time - start_time:.2f} seconds.\n"
)

# === STRATEGY SELECTION ===
# Choose clustering strategy: 'fcm_euclidean', 'fcm_mahalanobis', 'gustafson_kessel'
chosen_strategy = "gustafson_kessel"  # Change this to switch strategies

CLUSTERING_STRATEGIES = {
    "fcm_euclidean": lambda df: perform_fuzzy_clustering(
        df, distance_metric="euclidean", return_membership=True
    ),
    "fcm_mahalanobis": lambda df: perform_fuzzy_clustering(
        df, distance_metric="mahalanobis", return_membership=True
    ),
    "gustafson_kessel": lambda df: multi_run_fuzzy_clustering(
        df
    ),  # Changed to multi_run_fuzzy_clustering
}

# === Step 4: Clustering ===
start_time = time.time()
print(f"5.🧪 Performing clustering using strategy: {chosen_strategy} ...")
df["followers"] = df["followers"].fillna(0)
# Prepare feature matrix for silhouette score
features = [
    df["sentiment_score"],
    df["eigenvector_centrality"],
    df["closeness_centrality"],
    df["betweenness_centrality"],
    df["followers"],
    df["keyword_freq"],
    df["engagement"],
]
feature_matrix = np.vstack([f.fillna(0).to_numpy() for f in features])

result = CLUSTERING_STRATEGIES[chosen_strategy](df)
cluster_labels, centers, fpc, membership_matrix = (
    result  # Simplified as multi_run_fuzzy_clustering returns 4 values
)


# Map cluster index to readable risk categories
label_map = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
df["risk_category"] = [label_map.get(label, "Unknown") for label in cluster_labels]

# === Step 4.5: Flag borderline users ===
df["borderline_flag"] = pd.Series(np.max(membership_matrix, axis=0)).between(0.35, 0.65)

# === Step 4.6: Fuzzy silhouette score ===
sil_score = fuzzy_silhouette_score(feature_matrix, membership_matrix)
print(f"6. Fuzzy Silhouette Score: {sil_score:.3f}")
end_time = time.time()
print(f"   Time taken for Clustering: {end_time - start_time:.2f} seconds.\n")

# === Step 5: Store in MongoDB ===
start_time = time.time()
print("7. 💾 Saving classified users to MongoDB...")
records = df.to_dict(orient="records")
save_users_to_db(records)
end_time = time.time()
print(f"   Time taken for Storing in MongoDB: {end_time - start_time:.2f} seconds.\n")

# === Step 6: (Optional) Visualize ===
start_time = time.time()
print("8. 📈 Visualizing clusters...")
visualize_clusters(df, cluster_labels)
end_time = time.time()
print(f"   Time taken for Visualization: {end_time - start_time:.2f} seconds.\n")

print("9. ✅ Pipeline completed successfully.")
print(" ***********************  PROCESSING COMPLETED . **************************")
