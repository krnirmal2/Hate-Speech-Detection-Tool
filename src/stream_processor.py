from typing import Dict, Any
import json
from kafka import KafkaConsumer, KafkaProducer
from config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET
)
from logger import logger
from text_preprocessing import analyze_sentiment
from graph_analysis import build_social_graph, compute_centrality_metrics
from fuzzy_clustering import perform_fuzzy_clustering
from database import save_to_mongodb
from alerts import send_alert

class StreamProcessor:
    def __init__(self):
        """Initialize Kafka consumer and producer."""
        self.consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True
        )
        
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
        logger.info("Stream processor initialized")

    def process_tweet(self, tweet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single tweet through the pipeline.
        
        Args:
            tweet (Dict[str, Any]): Raw tweet data
            
        Returns:
            Dict[str, Any]: Processed tweet with analysis results
        """
        try:
            # Extract text and metadata
            text = tweet.get('text', '')
            username = tweet.get('user', {}).get('screen_name', '')
            
            # Perform sentiment analysis
            sentiment_score = analyze_sentiment(text)
            
            # Build social graph and compute metrics
            graph = build_social_graph([tweet])
            centrality = compute_centrality_metrics(graph)
            
            # Perform fuzzy clustering
            features = {
                'sentiment_score': sentiment_score,
                'eigenvector_centrality': centrality.get(username, 0),
                'followers_count': tweet.get('user', {}).get('followers_count', 0)
            }
            
            cluster_assignments, _, fpc = perform_fuzzy_clustering([features])
            
            # Prepare result
            result = {
                'tweet_id': tweet.get('id_str'),
                'username': username,
                'text': text,
                'sentiment_score': sentiment_score,
                'centrality_score': centrality.get(username, 0),
                'cluster': int(cluster_assignments[0]),
                'fpc': float(fpc),
                'timestamp': tweet.get('created_at')
            }
            
            # Save to MongoDB
            save_to_mongodb(result)
            
            # Send alert if necessary
            if sentiment_score < -0.5 or result['cluster'] == 2:  # High risk
                send_alert(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing tweet: {str(e)}")
            return None

    def start_processing(self):
        """Start the stream processing loop."""
        logger.info("Starting stream processing")
        
        try:
            for message in self.consumer:
                tweet = message.value
                result = self.process_tweet(tweet)
                
                if result:
                    # Send processed result to output topic
                    self.producer.send(
                        f"{KAFKA_TOPIC}_processed",
                        value=result
                    )
                    
        except KeyboardInterrupt:
            logger.info("Stopping stream processing")
        finally:
            self.consumer.close()
            self.producer.close()

if __name__ == "__main__":
    processor = StreamProcessor()
    processor.start_processing() 