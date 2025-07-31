import pytest
from unittest.mock import patch, MagicMock
import os
from src.repository.database import (
    get_mongo_client,
    save_users_to_db,
    get_users_by_risk,
)


# Mock environment variables for testing
@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {"MONGO_URI": "mongodb://localhost:27017/testdb"}):
        yield


# Mock MongoClient and database connection
@pytest.fixture
def mock_mongo_client():
    with patch("src.repository.database.MongoClient") as mock_client_class:
        mock_client_instance = MagicMock()  # This is what MongoClient() returns
        mock_db_instance = MagicMock()
        mock_collection_instance = MagicMock()

        mock_client_class.return_value = mock_client_instance
        mock_client_instance.__getitem__.return_value = mock_db_instance
        mock_db_instance.__getitem__.return_value = mock_collection_instance

        yield mock_client_class, mock_client_instance, mock_db_instance, mock_collection_instance


def test_get_database_success(mock_mongo_client):
    (
        mock_client_class,
        mock_client_instance,
        mock_db_instance,
        mock_collection_instance,
    ) = mock_mongo_client
    client = get_mongo_client()
    mock_client_class.assert_called_once_with("mongodb://localhost:27017/testdb")
    assert client is mock_client_instance
    assert client["hate_speech_detection"] is mock_db_instance


def test_save_classified_users(mock_mongo_client):
    (
        mock_client_class,
        mock_client_instance,
        mock_db_instance,
        mock_collection_instance,
    ) = mock_mongo_client
    save_users_to_db(
        [
            {"username": "user1", "risk_category": "High Risk"},
            {"username": "user2", "risk_category": "Low Risk"},
        ]
    )
    mock_collection_instance.insert_many.assert_called_once_with(
        [
            {"username": "user1", "risk_category": "High Risk"},
            {"username": "user2", "risk_category": "Low Risk"},
        ]
    )


def test_get_users_by_risk_category(mock_mongo_client):
    (
        mock_client_class,
        mock_client_instance,
        mock_db_instance,
        mock_collection_instance,
    ) = mock_mongo_client
    mock_collection_instance.find.return_value = [
        {"username": "userA", "risk_category": "High Risk"},
        {"username": "userB", "risk_category": "High Risk"},
    ]

    users = get_users_by_risk("High Risk")
    mock_collection_instance.find.assert_called_once_with(
        {"risk_category": "High Risk"}, {"_id": 0}
    )
    assert len(users) == 2
    assert users[0]["username"] == "userA"


def test_get_users_by_risk_category_empty(mock_mongo_client):
    (
        mock_client_class,
        mock_client_instance,
        mock_db_instance,
        mock_collection_instance,
    ) = mock_mongo_client
    mock_collection_instance.find.return_value = []

    users = get_users_by_risk("Low Risk")
    mock_collection_instance.find.assert_called_once_with(
        {"risk_category": "Low Risk"}, {"_id": 0}
    )
    assert len(users) == 0


def test_mongo_connection_success(mock_mongo_client):
    (
        mock_client_class,
        mock_client_instance,
        mock_db_instance,
        mock_collection_instance,
    ) = mock_mongo_client

    # Mock the admin.command('ismaster') call
    mock_client_instance.admin.command.return_value = {"ok": 1.0}

    client = get_mongo_client()
    client.admin.command("ismaster")
    mock_client_instance.admin.command.assert_called_once_with("ismaster")
    client.close()
    mock_client_instance.close.assert_called_once()
