# Consumes Kafka tweets, processes them
📄 Purpose:
# Listens to the Kafka topic
# Analyzes tweet → classifies → stores in MongoDB
# kafka/kafka_consumer.py

from kafka import KafkaConsumer
import json
import pandas as pd
from src.text_preprocessing import analyze_sentiment_bert
from src.database import save_users_to_db
from src.fuzzy_clustering import perform_fuzzy_clustering

consumer = KafkaConsumer(
    'twitter_stream',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

batch = []

for msg in consumer:
    tweet = msg.value
    sentiment = analyze_sentiment_bert(tweet['text'])

    row = {
        "username": tweet['username'],
        "text": tweet['text'],
        "sentiment_score": sentiment,
        "followers_count": tweet.get('followers_count', 0),
        "eigenvector_centrality": 0.5  # dummy or precomputed
    }

    batch.append(row)

    if len(batch) >= 10:
        df = pd.DataFrame(batch)
        cluster_labels, _, _ = perform_fuzzy_clustering(df)

        label_map = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
        df["risk_category"] = [label_map.get(lbl, "Unknown") for lbl in cluster_labels]

        save_users_to_db(df.to_dict("records"))
        batch.clear()
        print("✅ Batch processed and saved to DB")
