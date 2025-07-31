import pytest
import pandas as pd
import numpy as np
from src.service.clusteringStrategy.fuzzy_clustering import (
    normalize_series,
    perform_fuzzy_clustering,
    gustafson_kessel_clustering,
    fuzzy_silhouette_score,
)


@pytest.fixture
def sample_features_df():
    return pd.DataFrame(
        {
            "sentiment_score": [0.1, 0.9, 0.2, 0.8, 0.15, 0.85],
            "eigenvector_centrality": [0.01, 0.09, 0.02, 0.08, 0.015, 0.085],
            "closeness_centrality": [0.01, 0.09, 0.02, 0.08, 0.015, 0.085],
            "betweenness_centrality": [0.01, 0.09, 0.02, 0.08, 0.015, 0.085],
            "followers": [100, 1000, 150, 900, 120, 950],
            "keyword_freq": [0.1, 0.8, 0.2, 0.7, 0.15, 0.75],
            "engagement": [0.05, 0.5, 0.1, 0.4, 0.08, 0.45],
            "username": [f"user{i}" for i in range(6)],
        }
    )


def test_normalize_series():
    series = pd.Series([10, 20, 30, 0, 50])
    normalized = normalize_series(series)
    assert isinstance(normalized, pd.Series)
    assert normalized.min() >= 0 and normalized.max() <= 1
    assert normalized.iloc[3] == 0  # 0 should remain 0 if it's the min
    assert normalized.iloc[4] == 1  # 50 should become 1 if it's the max


def test_perform_fuzzy_clustering(sample_features_df):
    cluster_labels, centers, fpc, membership_matrix = perform_fuzzy_clustering(
        sample_features_df
    )
    assert isinstance(cluster_labels, np.ndarray)
    assert isinstance(centers, np.ndarray)
    assert isinstance(fpc, float)
    assert isinstance(membership_matrix, np.ndarray)
    assert len(cluster_labels) == len(sample_features_df)
    assert centers.shape[0] == 3  # Default 3 clusters
    assert fpc >= 0 and fpc <= 1
    assert membership_matrix.shape == (len(sample_features_df), 3)


def test_gustafson_kessel_clustering(sample_features_df):
    cluster_labels, centers, fpc, membership_matrix, covariances = (
        gustafson_kessel_clustering(sample_features_df)
    )
    assert isinstance(cluster_labels, np.ndarray)
    assert isinstance(centers, np.ndarray)
    assert isinstance(fpc, float)
    assert isinstance(membership_matrix, np.ndarray)
    assert isinstance(covariances, np.ndarray)
    assert len(cluster_labels) == len(sample_features_df)
    assert centers.shape[0] == 3  # Default 3 clusters
    assert fpc >= 0 and fpc <= 1
    assert membership_matrix.shape == (len(sample_features_df), 3)


def test_fuzzy_silhouette_score(sample_features_df):
    # Need to run a clustering algorithm first to get membership matrix
    _, _, _, membership_matrix = perform_fuzzy_clustering(sample_features_df)

    features = [
        sample_features_df["sentiment_score"],
        sample_features_df["eigenvector_centrality"],
        sample_features_df["closeness_centrality"],
        sample_features_df["betweenness_centrality"],
        sample_features_df["followers"],
        sample_features_df["keyword_freq"],
        sample_features_df["engagement"],
    ]
    feature_matrix = np.vstack([f.fillna(0).to_numpy() for f in features]).T

    sil_score = fuzzy_silhouette_score(feature_matrix, membership_matrix)
    assert isinstance(sil_score, float)
    assert sil_score >= -1 and sil_score <= 1


def test_perform_fuzzy_clustering_k_value():
    df = pd.DataFrame(
        {
            "sentiment_score": np.random.rand(10),
            "eigenvector_centrality": np.random.rand(10),
            "closeness_centrality": np.random.rand(10),
            "betweenness_centrality": np.random.rand(10),
            "followers": np.random.randint(10, 1000, 10),
            "keyword_freq": np.random.rand(10),
            "engagement": np.random.rand(10),
            "username": [f"user{i}" for i in range(10)],
        }
    )

    # Test with a different number of clusters (k=2)
    cluster_labels, centers, fpc, membership_matrix = perform_fuzzy_clustering(df, k=2)
    assert centers.shape[0] == 2
    assert membership_matrix.shape == (10, 2)
