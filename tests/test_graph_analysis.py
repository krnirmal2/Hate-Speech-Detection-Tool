import pytest
import pandas as pd
import networkx as nx
from src.service.graph_analysis import (
    build_social_graph,
    compute_all_centrality_metrics,
)


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame(
        {
            "username": ["userA", "userB", "userC", "userD"],
            "tweets": [
                "This is a tweet from userA mentioning @userB and @userC",
                "Another tweet by userB mentioning @userA",
                "UserC talks about userD",
                "UserD replies to @userC",
            ],
            "followers": [100, 200, 50, 150],
            "retweet_count": [10, 20, 5, 15],
            "reply_count": [2, 4, 1, 3],
            "sentiment_score": [0.5, -0.2, 0.8, -0.5],
        }
    )


def test_build_social_graph(sample_dataframe):
    G = build_social_graph(sample_dataframe)
    assert isinstance(G, nx.Graph)
    assert G.number_of_nodes() == 4
    assert (
        G.number_of_edges() >= 2
    )  # userA -> userB, userA -> userC, userB -> userA, userD -> userC
    assert ("userA", "userB") in G.edges or ("userB", "userA") in G.edges
    assert ("userA", "userC") in G.edges or ("userC", "userA") in G.edges


def test_build_social_graph_empty_df():
    empty_df = pd.DataFrame(
        columns=["username", "tweets", "followers", "retweet_count", "reply_count"]
    )
    G = build_social_graph(empty_df)
    assert isinstance(G, nx.Graph)
    assert G.number_of_nodes() == 0
    assert G.number_of_edges() == 0


def test_compute_all_centrality_metrics(sample_dataframe):
    G = build_social_graph(sample_dataframe)
    centralities = compute_all_centrality_metrics(G)

    assert isinstance(centralities, dict)
    assert "userA" in centralities
    assert "userB" in centralities
    assert "userC" in centralities
    assert "userD" in centralities

    for user_centralities in centralities.values():
        assert "eigenvector_centrality" in user_centralities
        assert "closeness_centrality" in user_centralities
        assert "betweenness_centrality" in user_centralities
        assert isinstance(user_centralities["eigenvector_centrality"], float)
        assert isinstance(user_centralities["closeness_centrality"], float)
        assert isinstance(user_centralities["betweenness_centrality"], float)


def test_compute_all_centrality_metrics_disconnected_graph():
    G = nx.Graph()
    G.add_nodes_from(["userX", "userY", "userZ"])
    centralities = compute_all_centrality_metrics(G)
    # For disconnected graphs, closeness and betweenness might be 0 or NaN depending on NetworkX version and specific implementation details for disconnected components
    # Eigenvector should be 0 for isolated nodes
    assert all(data["eigenvector_centrality"] == 0 for data in centralities.values())
    assert all(
        data["closeness_centrality"] == 0 for data in centralities.values()
    )  # or NaN, depending on networkx version and handling of disconnected components
    assert all(data["betweenness_centrality"] == 0 for data in centralities.values())
