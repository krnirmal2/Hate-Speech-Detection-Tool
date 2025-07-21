import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

# Create necessary directories
for dir_path in [DATA_DIR, MODELS_DIR, LOGS_DIR]:
    dir_path.mkdir(exist_ok=True)

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_WORKERS = int(os.getenv("API_WORKERS", "4"))

# Twitter API Configuration
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "hate_speech_detection")

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "tweets")

# Model Configuration
BERT_MODEL_NAME = "bert-base-uncased"
SENTIMENT_THRESHOLD = float(os.getenv("SENTIMENT_THRESHOLD", "-0.5"))
CLUSTER_THRESHOLD = float(os.getenv("CLUSTER_THRESHOLD", "0.7"))

# Alert Configuration
ALERT_EMAIL = os.getenv("ALERT_EMAIL")
ALERT_SLACK_WEBHOOK = os.getenv("ALERT_SLACK_WEBHOOK")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 