# Streams Twitter data to Kafka
# 📄 Purpose:
# Simulates live tweet ingestion using Kafka
# Sends tweets one by one from tweets_1.csv to the topic
# kafka/kafka_producer.py

from kafka import KafkaProducer
import pandas as pd
import json
import time

def load_sample_tweets(file_path="data/tweets_1.csv"):
    df = pd.read_csv(file_path)
    df = df.dropna(subset=["username", "text"])
    return df.to_dict(orient="records")

def send_to_kafka():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    tweets = load_sample_tweets()

    for tweet in tweets:
        producer.send('twitter_stream', value=tweet)
        print(f"✅ Tweet sent: {tweet['username']}")
        time.sleep(1)

if __name__ == "__main__":
    send_to_kafka()
