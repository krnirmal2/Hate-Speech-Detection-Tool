# MongoDB operations
📄 Purpose:
# Establish connection to MongoDB
# Insert records into a collection (users)
# Fetch users by risk_category

# src/database.py

from pymongo import MongoClient
from typing import List, Dict


def get_mongo_client(uri: str = "mongodb://localhost:27017/") -> MongoClient:
    """
    Establish MongoDB connection.

    Args:
        uri (str): MongoDB connection URI

    Returns:
        MongoClient: Connected client
    """
    return MongoClient(uri)


def save_users_to_db(users: List[Dict], db_name: str = "jihadist_detection", collection_name: str = "users"):
    """
    Inserts user records into MongoDB collection.

    Args:
        users (List[Dict]): List of user records (risk tagged)
        db_name (str): Database name
        collection_name (str): Collection name
    """
    client = get_mongo_client()
    db = client[db_name]
    collection = db[collection_name]

    if users:
        collection.insert_many(users)
        print(f"✅ Inserted {len(users)} users into DB.")
    else:
        print("⚠️ No users to insert.")


def get_users_by_risk(risk_level: str, db_name: str = "jihadist_detection", collection_name: str = "users") -> List[Dict]:
    """
    Fetches users from DB by risk category.

    Args:
        risk_level (str): 'High Risk', 'Medium Risk', or 'Low Risk'
        db_name (str): Database name
        collection_name (str): Collection name

    Returns:
        List[Dict]: List of users in the specified category
    """
    client = get_mongo_client()
    db = client[db_name]
    collection = db[collection_name]

    users = list(collection.find({"risk_category": risk_level}, {"_id": 0}))
    return users

# {
#   "username": "radical_guy123",
#   "text": "We will rise soon. #Jihad",
#   "followers_count": 950,
#   "sentiment_score": -0.9,
#   "eigenvector_centrality": 0.82,
#   "risk_category": "High Risk"
# }
