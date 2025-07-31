import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.controller.api import app  # Assuming 'app' is the FastAPI instance

client = TestClient(app)


@pytest.fixture
def mock_dependencies():
    with (
        patch("src.repository.database.get_users_by_risk_category") as mock_get_users,
        patch("src.text_preprocessing.analyze_sentiment_bert") as mock_sentiment,
        patch(
            "src.service.clusteringStrategy.fuzzy_clustering.perform_fuzzy_clustering"
        ) as mock_clustering,
        patch("src.repository.database.save_classified_users") as mock_save_users,
        patch(
            "src.service.graph_analysis.build_social_graph"
        ) as mock_build_graph,  # Mocking this for analyze_tweet
        patch(
            "src.service.graph_analysis.compute_all_centrality_metrics"
        ) as mock_centrality,  # Mocking this for analyze_tweet
    ):
        yield mock_get_users, mock_sentiment, mock_clustering, mock_save_users, mock_build_graph, mock_centrality


def test_get_users_by_risk_category_high_risk(mock_dependencies):
    mock_get_users, _, _, _, _, _ = mock_dependencies
    mock_get_users.return_value = [
        {"username": "userH1", "risk_category": "High Risk"},
        {"username": "userH2", "risk_category": "High Risk"},
    ]
    response = client.get("/users/High Risk")
    assert response.status_code == 200
    assert response.json() == [
        {"username": "userH1", "risk_category": "High Risk"},
        {"username": "userH2", "risk_category": "High Risk"},
    ]
    mock_get_users.assert_called_once_with("High Risk")


def test_get_users_by_risk_category_low_risk(mock_dependencies):
    mock_get_users, _, _, _, _, _ = mock_dependencies
    mock_get_users.return_value = [{"username": "userL1", "risk_category": "Low Risk"}]
    response = client.get("/users/Low Risk")
    assert response.status_code == 200
    assert response.json() == [{"username": "userL1", "risk_category": "Low Risk"}]
    mock_get_users.assert_called_once_with("Low Risk")


def test_get_users_by_risk_category_invalid_category(mock_dependencies):
    mock_get_users, _, _, _, _, _ = mock_dependencies
    response = client.get("/users/Invalid Category")
    assert response.status_code == 422  # FastAPI validation error for Enum


def test_analyze_tweet_success(mock_dependencies):
    (
        mock_get_users,
        mock_sentiment,
        mock_clustering,
        mock_save_users,
        mock_build_graph,
        mock_centrality,
    ) = mock_dependencies

    mock_sentiment.return_value = 0.9  # High sentiment

    # Mock fuzzy clustering to return a specific cluster label (e.g., High Risk)
    # It expects (cluster_labels, centers, fpc, membership_matrix)
    mock_clustering.return_value = (
        np.array([2]),
        None,
        0.9,
        np.array([[0.1, 0.1, 0.8]]),
    )

    # Mock graph analysis outputs - necessary for the full pipeline within analyze_tweet
    mock_build_graph.return_value = MagicMock()
    mock_centrality.return_value = {
        "mock_user": {
            "eigenvector_centrality": 0.5,
            "closeness_centrality": 0.5,
            "betweenness_centrality": 0.5,
        }
    }

    tweet_data = {
        "tweet_text": "This is a test tweet about extremism.",
        "username": "test_user",
        "followers": 100,
        "retweet_count": 5,
        "reply_count": 2,
    }
    response = client.post("/analyze_tweet", json=tweet_data)

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["username"] == "test_user"
    assert response_json["risk_category"] == "High Risk"
    assert "sentiment_score" in response_json
    assert "eigenvector_centrality" in response_json  # Ensure centrality is present
    assert "closeness_centrality" in response_json
    assert "betweenness_centrality" in response_json
    assert "keyword_freq" in response_json
    assert "engagement" in response_json
    assert "fpc" in response_json

    mock_sentiment.assert_called_once_with(tweet_data["tweet_text"])
    mock_save_users.assert_called_once()  # Should save the classified user


def test_analyze_tweet_missing_fields():
    response = client.post("/analyze_tweet", json={"tweet_text": "just a tweet"})
    assert (
        response.status_code == 422
    )  # Unprocessable Entity due to missing required fields


def test_analyze_tweet_no_username_in_graph_data(mock_dependencies):
    (
        mock_get_users,
        mock_sentiment,
        mock_clustering,
        mock_save_users,
        mock_build_graph,
        mock_centrality,
    ) = mock_dependencies
    mock_sentiment.return_value = 0.1
    mock_clustering.return_value = (
        np.array([0]),
        None,
        0.5,
        np.array([[0.8, 0.1, 0.1]]),
    )

    # Mock centrality to return an empty dict, simulating username not found in graph
    mock_centrality.return_value = {}

    tweet_data = {
        "tweet_text": "neutral tweet",
        "username": "unknown_user",  # This user won't be in the mocked centrality
        "followers": 50,
        "retweet_count": 1,
        "reply_count": 0,
    }
    response = client.post("/analyze_tweet", json=tweet_data)
    assert response.status_code == 200
    response_json = response.json()
    # Ensure default 0.0 for centrality if user not found in graph
    assert response_json["eigenvector_centrality"] == 0.0
    assert response_json["closeness_centrality"] == 0.0
    assert response_json["betweenness_centrality"] == 0.0
