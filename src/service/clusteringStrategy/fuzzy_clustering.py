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


def perform_fuzzy_clustering(
    df: pd.DataFrame,
    num_clusters: int = 3,
    distance_metric: str = "euclidean",
    return_membership: bool = False,
):
    """
    Clusters users based on sentiment, centralities, and followers using fuzzy C-means.

    Args:
        df (pd.DataFrame): Input dataframe containing 'sentiment_score',
                           'eigenvector_centrality', 'closeness_centrality',
                           'betweenness_centrality', 'followers'
        num_clusters (int): Number of risk categories (e.g., 3)
        distance_metric (str): 'euclidean' or 'mahalanobis'
        return_membership (bool): If True, also return the membership matrix (u)

    Returns:
        list: Cluster assignment per user
        np.ndarray: Cluster centers
        float: Fuzzy Partition Coefficient (FPC)
        (optional) np.ndarray: Membership matrix (u)
    """
    # Normalize input features
    features = [
        normalize_series(df["sentiment_score"]),
        normalize_series(df["eigenvector_centrality"]),
        normalize_series(df["closeness_centrality"]),
        normalize_series(df["betweenness_centrality"]),
        normalize_series(df["followers"]),
    ]
    data = np.vstack(features)

    if distance_metric == "mahalanobis":
        # Compute covariance matrix and its inverse
        cov = np.cov(data)
        inv_cov = np.linalg.pinv(cov)
        # Mahalanobis transform: x' = L^-1 x, where L is Cholesky of cov
        L = np.linalg.cholesky(cov + 1e-6 * np.eye(cov.shape[0]))
        L_inv = np.linalg.inv(L)
        data = L_inv @ data

    # Apply fuzzy c-means clustering
    cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
        data=data, c=num_clusters, m=2.0, error=0.005, maxiter=1000, init=None
    )

    # Get the most likely cluster for each user
    cluster_assignments = np.argmax(u, axis=0)

    if return_membership:
        return cluster_assignments, cntr, fpc, u
    return cluster_assignments, cntr, fpc


def multi_run_fuzzy_clustering(
    df: pd.DataFrame,
    num_clusters: int = 3,
    distance_metric: str = "euclidean",
    n_runs: int = 10,
):
    """
    Runs fuzzy clustering n times and averages the membership matrices and centers.
    Returns the averaged cluster assignments, centers, FPC, and membership matrix.
    """
    all_memberships = []
    all_centers = []
    all_fpcs = []
    for i in range(n_runs):
        # Optionally, set a different random seed each time
        np.random.seed(i)
        cluster_labels, centers, fpc, u = perform_fuzzy_clustering(
            df, num_clusters, distance_metric, return_membership=True
        )
        all_memberships.append(u)
        all_centers.append(centers)
        all_fpcs.append(fpc)
    avg_membership = np.mean(all_memberships, axis=0)
    avg_centers = np.mean(all_centers, axis=0)
    avg_fpc = np.mean(all_fpcs)
    cluster_assignments = np.argmax(avg_membership, axis=0)
    return cluster_assignments, avg_centers, avg_fpc, avg_membership


from sklearn.metrics import pairwise_distances


def fuzzy_silhouette_score(data, membership_matrix):
    """
    Computes a fuzzy-adapted silhouette score for clustering quality.
    data: (features x samples) numpy array
    membership_matrix: (clusters x samples) numpy array
    Returns: average silhouette score
    """
    data = data.T  # samples x features
    n_samples = data.shape[0]
    n_clusters = membership_matrix.shape[0]
    distances = pairwise_distances(data)
    silhouettes = []
    for i in range(n_samples):
        u_i = membership_matrix[:, i]
        a = 0
        for k in range(n_clusters):
            # Intra-cluster distance weighted by membership
            members = np.where(np.argmax(membership_matrix, axis=0) == k)[0]
            if len(members) > 1:
                a_k = np.mean([distances[i, j] for j in members if j != i])
                a += u_i[k] * a_k
        # Inter-cluster distance
        b = np.inf
        for k in range(n_clusters):
            members = np.where(np.argmax(membership_matrix, axis=0) == k)[0]
            if len(members) > 0:
                b_k = np.mean([distances[i, j] for j in members])
                if b_k < b:
                    b = b_k
        s = (b - a) / max(a, b) if max(a, b) > 0 else 0
        silhouettes.append(s)
    return np.mean(silhouettes)


def visualize_clusters(df: pd.DataFrame, cluster_labels: list):
    """
    Visualizes clustering results in 2D.

    Args:
        df (pd.DataFrame): Original data with features
        cluster_labels (list): Cluster assignments
    """
    plt.figure(figsize=(8, 5))
    scatter = plt.scatter(
        df["eigenvector_centrality"],
        df["sentiment_score"],
        c=cluster_labels,
        cmap="viridis",
        alpha=0.7,
    )
    plt.xlabel("Eigenvector Centrality")
    plt.ylabel("Sentiment Score")
    plt.title("Fuzzy Clustering of Users (Influence vs. Sentiment)")
    plt.colorbar(scatter, label="Cluster")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def gustafson_kessel_clustering(
    df: pd.DataFrame,
    num_clusters: int = 3,
    m: float = 2.0,
    maxiter: int = 1000,
    error: float = 1e-5,
):
    """
    Gustafson-Kessel fuzzy clustering with per-cluster covariance matrices.
    Args:
        df: DataFrame with features (each row = sample)
        num_clusters: number of clusters
        m: fuzziness parameter
        maxiter: max iterations
        error: convergence tolerance
    Returns:
        cluster_assignments, centers, FPC, membership_matrix, covariances
    """
    # Prepare data matrix (features x samples)
    features = [
        normalize_series(df["sentiment_score"]),
        normalize_series(df["eigenvector_centrality"]),
        normalize_series(df["closeness_centrality"]),
        normalize_series(df["betweenness_centrality"]),
        normalize_series(df["followers"]),
        normalize_series(df["keyword_freq"]),
        normalize_series(df["engagement"]),
    ]
    X = np.vstack(features).T  # samples x features
    N = X.shape[0]
    d = X.shape[1]
    c = num_clusters
    # Initialize membership matrix randomly
    u = np.random.dirichlet(np.ones(c), size=N).T  # c x N
    centers = np.zeros((c, d))
    covariances = np.array([np.eye(d) for _ in range(c)])
    for iteration in range(maxiter):
        u_old = u.copy()
        # Update centers
        for k in range(c):
            um = u[k] ** m
            centers[k] = np.sum(um[:, None] * X, axis=0) / np.sum(um)
        # Update covariances
        for k in range(c):
            um = u[k] ** m
            diff = X - centers[k]
            cov = np.dot((um[:, None] * diff).T, diff) / np.sum(um)
            # Regularize to avoid singularity
            cov += 1e-6 * np.eye(d)
            covariances[k] = cov
        # Update distances
        dist = np.zeros((c, N))
        for k in range(c):
            diff = X - centers[k]
            inv_cov = np.linalg.pinv(covariances[k])
            dist[k] = np.sqrt(np.sum(diff @ inv_cov * diff, axis=1))
        # Avoid division by zero
        dist = np.fmax(dist, 1e-10)
        # Update membership
        for k in range(c):
            denom = np.sum((dist[k][:, None] / dist.T) ** (2 / (m - 1)), axis=1)
            u[k] = 1.0 / denom
        # Check convergence
        if np.linalg.norm(u - u_old) < error:
            break
    # Fuzzy Partition Coefficient
    fpc = np.sum(u**2) / N
    cluster_assignments = np.argmax(u, axis=0)
    return cluster_assignments, centers, fpc, u, covariances
