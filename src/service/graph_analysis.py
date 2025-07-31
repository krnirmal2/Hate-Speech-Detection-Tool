# Social graph construction using NetworkX
# 📄 Purpose:
# Build a directed social graph from mentions and retweets
# Compute centrality metrics using NetworkX:
# Eigenvector Centrality
# Betweenness Centrality
# Degree Centrality


# src/graph_analysis.py

import networkx as nx
import pandas as pd
import re


def build_social_graph(df: pd.DataFrame) -> nx.DiGraph:
    """
    Constructs a directed social graph using tweet mentions and retweets.

    Args:
        df (pd.DataFrame): Cleaned tweet dataset

    Returns:
        nx.DiGraph: Social network graph
    """
    G = nx.DiGraph()

    for _, row in df.iterrows():
        user = row["username"]
        tweet = row.get("tweets", "")  # <-- Add this line

        G.add_node(user)

        if isinstance(tweet, str):
            mentions = re.findall(
                r"@[\w_]+", tweet
            )  # Extract @mentions like @user_name
            for mention in mentions:
                mentioned_user = mention[1:]  # remove '@'
                G.add_edge(user, mentioned_user)

    return G


def compute_centrality_metrics(G: nx.DiGraph) -> dict:
    """
    Computes eigenvector centrality for all users in the graph.

    Args:
        G (nx.DiGraph): Social graph

    Returns:
        dict: Username to eigenvector centrality score
    """
    try:
        eigen_centrality = nx.eigenvector_centrality_numpy(G)
    except nx.PowerIterationFailedConvergence:
        eigen_centrality = nx.eigenvector_centrality(G, max_iter=1000)

    return eigen_centrality


def find_root_propagator(G: nx.DiGraph) -> str:
    """
    Finds the original propagator with no incoming edges.

    Args:
        G (nx.DiGraph): Social graph

    Returns:
        str: Username of root propagator
    """
    for node in G.nodes:
        if G.in_degree(node) == 0:
            return node
    return None


def compute_all_centrality_metrics(G: nx.DiGraph) -> dict:
    """
    Computes eigenvector, closeness, and betweenness centrality for all users in the graph.

    Args:
        G (nx.DiGraph): Social graph

    Returns:
        dict: Username to dict of centrality scores
    """
    try:
        eigen_centrality = nx.eigenvector_centrality_numpy(G)
    except nx.PowerIterationFailedConvergence:
        eigen_centrality = nx.eigenvector_centrality(G, max_iter=1000)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

    # Combine all metrics per user
    all_metrics = {}
    for node in G.nodes:
        all_metrics[node] = {
            "eigenvector_centrality": eigen_centrality.get(node, 0),
            "closeness_centrality": closeness_centrality.get(node, 0),
            "betweenness_centrality": betweenness_centrality.get(node, 0),
        }
    return all_metrics


# build_social_graph(df) → returns a directed graph

# compute_centrality_metrics(G) → returns a user: score mapping

# find_root_propagator(G) → identifies first user with no incoming edges
