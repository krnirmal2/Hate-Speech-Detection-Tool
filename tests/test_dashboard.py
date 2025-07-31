import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.dashboard.dashboard import (
    get_user_risk_distribution,
    get_top_influential_users,
    get_classified_tweets_data,
    get_live_updates_from_mongodb,
)


@pytest.fixture
def mock_database_functions():
    with (
        patch("src.repository.database.get_database") as mock_get_db,
        patch(
            "src.repository.database.get_users_by_risk_category"
        ) as mock_get_users_by_risk,
        patch("src.repository.database.get_all_classified_users") as mock_get_all_users,
    ):
        # Mock MongoDB collection object and its methods
        mock_classified_users_collection = MagicMock()
        mock_classified_users_collection.aggregate.return_value.to_list.return_value = [
            {"_id": "High Risk", "count": 5},
            {"_id": "Medium Risk", "count": 3},
            {"_id": "Low Risk", "count": 2},
        ]

        mock_db = MagicMock()
        mock_db.classified_users = mock_classified_users_collection
        mock_get_db.return_value = mock_db

        yield mock_get_users_by_risk, mock_get_all_users, mock_classified_users_collection


def test_get_user_risk_distribution(mock_database_functions):
    _, _, mock_classified_users_collection = mock_database_functions
    distribution = get_user_risk_distribution()

    expected_distribution = {"High Risk": 5, "Medium Risk": 3, "Low Risk": 2}
    assert distribution == expected_distribution
    mock_classified_users_collection.aggregate.assert_called_once()


def test_get_top_influential_users(mock_database_functions):
    mock_get_users_by_risk, _, _ = mock_database_functions
    mock_get_users_by_risk.return_value = [
        {
            "username": "userA",
            "followers": 1000,
            "eigenvector_centrality": 0.8,
            "closeness_centrality": 0.5,
            "betweenness_centrality": 0.3,
        },
        {
            "username": "userB",
            "followers": 2000,
            "eigenvector_centrality": 0.9,
            "closeness_centrality": 0.6,
            "betweenness_centrality": 0.4,
        },
        {
            "username": "userC",
            "followers": 500,
            "eigenvector_centrality": 0.7,
            "closeness_centrality": 0.4,
            "betweenness_centrality": 0.2,
        },
    ]

    top_users = get_top_influential_users()
    assert isinstance(top_users, pd.DataFrame)
    assert not top_users.empty
    assert len(top_users) == 3
    # Check sorting by eigenvector_centrality (descending)
    assert top_users.iloc[0]["username"] == "userB"
    assert top_users.iloc[1]["username"] == "userA"
    assert top_users.iloc[2]["username"] == "userC"
    mock_get_users_by_risk.assert_called_once_with(
        None
    )  # Called with None to get all users


def test_get_classified_tweets_data(mock_database_functions):
    _, mock_get_all_users, _ = mock_database_functions
    mock_get_all_users.return_value = [
        {
            "username": "user1",
            "tweet_text": "tweet1",
            "risk_category": "High Risk",
            "sentiment_score": 0.9,
            "eigenvector_centrality": 0.5,
        },
        {
            "username": "user2",
            "tweet_text": "tweet2",
            "risk_category": "Low Risk",
            "sentiment_score": 0.1,
            "eigenvector_centrality": 0.1,
        },
    ]

    tweet_data = get_classified_tweets_data()
    assert isinstance(tweet_data, pd.DataFrame)
    assert not tweet_data.empty
    assert len(tweet_data) == 2
    assert "username" in tweet_data.columns
    assert "tweet_text" in tweet_data.columns
    mock_get_all_users.assert_called_once()


def test_get_live_updates_from_mongodb(mock_database_functions):
    mock_get_users_by_risk, mock_get_all_users, mock_classified_users_collection = (
        mock_database_functions
    )
    # Reset mocks for this specific test as it calls functions internally
    mock_get_users_by_risk.reset_mock()
    mock_get_all_users.reset_mock()
    mock_classified_users_collection.aggregate.reset_mock()

    mock_get_users_by_risk.return_value = [
        {
            "username": "userX",
            "followers": 100,
            "eigenvector_centrality": 0.8,
            "closeness_centrality": 0.5,
            "betweenness_centrality": 0.3,
        }
    ]
    mock_get_all_users.return_value = [
        {
            "username": "userX",
            "tweet_text": "tweetX",
            "risk_category": "High Risk",
            "sentiment_score": 0.9,
            "eigenvector_centrality": 0.8,
        }
    ]
    mock_classified_users_collection.aggregate.return_value.to_list.return_value = [
        {"_id": "High Risk", "count": 1}
    ]

    risk_dist, top_users, tweet_df = get_live_updates_from_mongodb()

    assert risk_dist == {"High Risk": 1}
    assert not top_users.empty
    assert not tweet_df.empty
    mock_get_users_by_risk.assert_called_once_with(None)
    mock_get_all_users.assert_called_once()
    mock_classified_users_collection.aggregate.assert_called_once()
