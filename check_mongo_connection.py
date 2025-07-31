import os
import sys
from pymongo.errors import ConnectionFailure

# Add the src directory to the Python path to allow imports from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from repository.database import get_mongo_client


def check_mongo_connection():
    try:
        client = get_mongo_client()
        client.admin.command("ismaster")
        print("MongoDB connection successful!")
        db = client["local"]
        collection = db["hate_speech_detection"]
        count = collection.count_documents({})
        print(f"Number of documents in hate_speech_detection: {count}")
        client.close()
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    check_mongo_connection()
