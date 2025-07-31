import pandas as pd
import numpy as np
from src.text_preprocessing import (
    analyze_sentiment_bert,
    keyword_frequency,
    engagement_metric,
)
from src.graph_analysis import build_social_graph, compute_all_centrality_metrics
from src.fuzzy_clustering import (
    perform_fuzzy_clustering,
    gustafson_kessel_clustering,
    fuzzy_silhouette_score,
)

# --- 1. Load or create a small sample dataset ---
# For demonstration, create a synthetic dataset if not present
try:
    df = pd.read_csv("data/twitter_sentiment_analysis.csv").sample(50, random_state=42)
except Exception:
    # Synthetic fallback
    df = pd.DataFrame(
        {
            "username": [f"user{i}" for i in range(10)],
            "tweets": [
                "Jihad caliphate martyrdom" if i % 2 == 0 else "Peace love unity"
                for i in range(10)
            ],
            "followers": np.random.randint(10, 1000, 10),
            "retweet_count": np.random.randint(0, 20, 10),
            "reply_count": np.random.randint(0, 10, 10),
        }
    )

# --- 2. Preprocessing ---
df["sentiment_score"] = df["tweets"].apply(analyze_sentiment_bert)
df["keyword_freq"] = df["tweets"].apply(keyword_frequency)
if "retweet_count" not in df.columns:
    df["retweet_count"] = 0
if "reply_count" not in df.columns:
    df["reply_count"] = 0
df["engagement"] = df.apply(engagement_metric, axis=1)

# --- 3. Graph and Centrality ---
G = build_social_graph(df)
centralities = compute_all_centrality_metrics(G)
for metric in [
    "eigenvector_centrality",
    "closeness_centrality",
    "betweenness_centrality",
]:
    df[metric] = (
        df["username"].map(lambda u: centralities.get(u, {}).get(metric, 0)).fillna(0)
    )

# --- 4. Clustering strategies ---
STRATEGIES = {
    "fcm_euclidean": lambda df: perform_fuzzy_clustering(
        df, distance_metric="euclidean", return_membership=True
    ),
    "fcm_mahalanobis": lambda df: perform_fuzzy_clustering(
        df, distance_metric="mahalanobis", return_membership=True
    ),
    "gustafson_kessel": lambda df: gustafson_kessel_clustering(df),
}

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

for strategy, func in STRATEGIES.items():
    print(f"\n=== Running strategy: {strategy} ===")
    if strategy == "gustafson_kessel":
        cluster_labels, centers, fpc, membership_matrix, covariances = func(df)
    else:
        cluster_labels, centers, fpc, membership_matrix = func(df)
    label_map = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
    df[f"risk_category_{strategy}"] = [
        label_map.get(label, "Unknown") for label in cluster_labels
    ]
    df[f"borderline_flag_{strategy}"] = pd.Series(
        np.max(membership_matrix, axis=0)
    ).between(0.35, 0.65)
    sil_score = fuzzy_silhouette_score(feature_matrix, membership_matrix)
    print(f"Fuzzy Partition Coefficient (FPC): {fpc:.3f}")
    print(f"Fuzzy Silhouette Score: {sil_score:.3f}")
    print(f"Borderline users: {df[f'borderline_flag_{strategy}'].sum()} / {len(df)}")
    # Print top suspicious nodes (High Risk, high centrality)
    suspicious = df[
        (df[f"risk_category_{strategy}"] == "High Risk")
        & (df["eigenvector_centrality"] > 0.1)
    ]
    print(f"Suspicious nodes (High Risk & high centrality):")
    print(
        suspicious[["username", "eigenvector_centrality", f"risk_category_{strategy}"]]
    )
    # Save report
    df.to_csv(f"test_report_{strategy}.csv", index=False)
    print(f"Report saved to test_report_{strategy}.csv")

print("\nAll strategies tested. See CSVs for detailed results.")
