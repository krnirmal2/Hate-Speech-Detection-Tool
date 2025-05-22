# Fuzzy C-Means and Gustafson-Kessel
# 📄 Purpose:
# Use skfuzzy to cluster users into low, medium, high risk
# Automatically compute Fuzzy Partition Coefficient (FPC)
# Returns:
# Cluster assignments
# FPC value
# Cluster centers

# src/fuzzy_clustering.py

import numpy as np
import skfuzzy as fuzz
import pandas as pd
import matplotlib.pyplot as plt

def normalize_series(series: pd.Series) -> pd.Series:
    """
    Normalizes a pandas series between 0 and 1.
    """
    min_val = series.min()
    max_val = series.max()
    return (series - min_val) / (max_val - min_val + 1e-9)

def perform_fuzzy_clustering(df: pd.DataFrame, num_clusters: int = 3):
    """
    Clusters users based on sentiment, influence and followers using fuzzy C-means.

    Args:
        df (pd.DataFrame): Input dataframe containing 'sentiment_score', 
                           'eigenvector_centrality', 'followers_count'
        num_clusters (int): Number of risk categories (e.g., 3)

    Returns:
        list: Cluster assignment per user
        np.ndarray: Cluster centers
        float: Fuzzy Partition Coefficient (FPC)
    """
    # Normalize input features
    sentiment = normalize_series(df['sentiment_score'])
    centrality = normalize_series(df['eigenvector_centrality'])
    followers = normalize_series(df['followers_count'])

    # Combine all features into a 2D array
    data = np.vstack([sentiment, centrality, followers])

    # Apply fuzzy c-means clustering
    cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
        data=data,
        c=num_clusters,
        m=2.0,
        error=0.005,
        maxiter=1000,
        init=None
    )

    # Get the most likely cluster for each user
    cluster_assignments = np.argmax(u, axis=0)

    return cluster_assignments, cntr, fpc


def visualize_clusters(df: pd.DataFrame, cluster_labels: list):
    """
    Visualizes clustering results in 2D.

    Args:
        df (pd.DataFrame): Original data with features
        cluster_labels (list): Cluster assignments
    """
    plt.figure(figsize=(8, 5))
    scatter = plt.scatter(
        df['eigenvector_centrality'],
        df['sentiment_score'],
        c=cluster_labels,
        cmap='viridis',
        alpha=0.7
    )
    plt.xlabel("Eigenvector Centrality")
    plt.ylabel("Sentiment Score")
    plt.title("Fuzzy Clustering of Users (Influence vs. Sentiment)")
    plt.colorbar(scatter, label='Cluster')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


