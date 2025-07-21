# 🚨 Jihadist Detection System

This system detects jihadist/extremist activity on Twitter using advanced AI, graph theory, and fuzzy clustering techniques.

---

## 📌 Key Features

- ✅ **Sentiment Analysis** using BERT
- ✅ **Social Graph Analysis** (NetworkX)
- ✅ **Fuzzy Clustering** (Fuzzy C-Means + Gustafson-Kessel)
- ✅ **MongoDB** Storage
- ✅ **FastAPI** for Real-time Classification & Querying
- ✅ **Streamlit** Dashboard for Risk Visualization
- ✅ **Kafka** for Real-time Tweet Streaming
- ✅ **Email Alerting** on extremist spikes
- ✅ **Docker + Kubernetes** Deployment Ready

---

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run core pipeline
python main.py

# 3. Start the API
uvicorn src.api:app --reload

# 4. Launch Dashboard
streamlit run dashboard/dashboard.py

```

## Features

- Real-time tweet processing using Kafka
- BERT-based sentiment analysis
- Social network analysis with NetworkX
- Fuzzy clustering for risk assessment
- MongoDB for data storage
- FastAPI backend
- Streamlit dashboard
- Prometheus monitoring
- Docker containerization

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Twitter API credentials
- MongoDB
- Kafka

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hate-speech-detection-tool.git
cd hate-speech-detection-tool
```

2. Create a `.env` file:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

## Usage

- FastAPI backend: http://localhost:8000
- Streamlit dashboard: http://localhost:8501
- Prometheus metrics: http://localhost:9090
- Grafana dashboard: http://localhost:3000

## Project Structure

```
hate-speech-detection-tool/
├── src/
│   ├── api.py              # FastAPI endpoints
│   ├── config.py           # Configuration
│   ├── dashboard.py        # Streamlit dashboard
│   ├── database.py         # MongoDB operations
│   ├── fuzzy_clustering.py # Fuzzy C-means clustering
│   ├── graph_analysis.py   # Network analysis
│   ├── logger.py           # Logging setup
│   ├── monitoring.py       # Prometheus metrics
│   ├── stream_processor.py # Kafka stream processing
│   └── text_preprocessing.py # BERT sentiment analysis
├── tests/                  # Test suite
├── data/                   # Data directory
├── models/                 # Model files
├── logs/                   # Log files
├── Dockerfile
├── docker-compose.yml
├── prometheus.yml
├── requirements.txt
└── README.md
```

## Development

1. Install development dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
pytest tests/
```

3. Run linting:
```bash
flake8 src/ tests/
```

## Monitoring

The system includes Prometheus metrics for:
- Total tweets processed
- Tweets by risk level
- Processing time
- Sentiment scores
- User centrality scores

## Security

- API keys stored in environment variables
- Rate limiting on API endpoints
- Input validation
- Authentication and authorization
- Secure MongoDB connection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

├── data/
│   └── tweets_1.csv              # Kaggle dataset
├── src/
│   ├── data_loader.py            # Load & clean data
│   ├── text_preprocessing.py     # Sentiment analysis using BERT
│   ├── graph_analysis.py         # NetworkX social graph logic
│   ├── fuzzy_clustering.py       # Fuzzy C-Means + Gustafson-Kessel
│   ├── database.py               # MongoDB integration
│   ├── api.py                    # FastAPI for querying
│   ├── topic_modeling.py         # LDA for topic detection
├── dashboard/
│   └── dashboard.py              # Streamlit UI
├── kafka/
│   ├── kafka_producer.py         # Twitter → Kafka
│   ├── kafka_consumer.py         # Kafka → pipeline
├── alerts/
│   └── alerts.py                 # Real-time alert system
├── deployment/
│   ├── Dockerfile.api
│   ├── Dockerfile.dashboard
│   ├── Dockerfile.producer
│   ├── Dockerfile.consumer
│   └── docker-compose.yml
├── config/
│   └── mongo_config.json
├── requirements.txt
├── README.md
├── HLD.md
├── LLD.md
└── main.py       



1. Project Overview
This project focuses on detecting extremist propaganda on social networks (especially Twitter) using Big Data, Graph Theory, and Fuzzy Clustering techniques. The goal is to:
	• Identify influential users spreading jihadist propaganda.
	• Classify users based on their activity, impact, and sentiment.
	• Monitor suspicious profiles in real time using machine learning.
Use Cases Beyond Terrorism Detection
	• HR departments for candidate profiling.
	• Security teams for detecting fraud in finance & insurance.
	• Immigration officers for flagging high-risk individuals.

2. Methodology
Step 1: Data Collection
	• Sources: 
		○ Kaggle datasets ("How ISIS Uses Twitter").
		○ Twitter's API REST & Streaming to fetch real-time tweets.
		○ ISIS-linked forums (Wafa Media Foundation) for vocabulary extraction.
	• Data Fields Extracted: 
		○ Usernames, tweet timestamps, followers, retweets, and mentions.
Step 2: Data Preprocessing
	• Filtering out irrelevant fields (e.g., fake usernames, location).
	• Feature Engineering: 
		○ Frequency of tweets to measure user activity.
		○ Sentiment analysis using VADER Lexicon & NLTK.
		○ Retweet/Mention Network to map social connections.
Step 3: Social Network Graph Analysis
	• Construct a Graph (Nodes = users, Edges = interactions).
	• Apply Centrality Measures: 
		○ Degree Centrality → Measures user's connections.
		○ Betweenness Centrality → Identifies information bridges.
		○ Eigenvector Centrality → Finds hierarchical influencers.
	• Visualizing relationships between users using Network Graphs.
Step 4: Fuzzy Clustering
	• Why Fuzzy Clustering? 
		○ Traditional classification is binary (terrorist or non-terrorist), but fuzzy logic provides a probability-based classification.
	• Algorithm Used: 
		○ Fuzzy C-Means Clustering with different distance metrics (Euclidean, Mahalanobis, Gustafson-Kessel).
	• Clusters Identified: 
		○ Highly Active Users (Red)
		○ Low-Risk Users (Blue)
		○ Ambiguous Users (Borderline Cases)
Step 5: Monitoring Suspicious Users
	• Users with low certainty scores (35%-65%) are flagged for continuous monitoring.
	• Helps in tracking radicalization trends over time.

3. Implementation Technologies
Component	Technology Used
Data Extraction	Kaggle Datasets, Twitter API, Python
Data Preprocessing	Python (NLTK, Regular Expressions)
Graph Analysis	NetworkX (Python Library)
Machine Learning	Fuzzy C-Means Clustering (SciPy, Scikit-learn)
Visualization	Matplotlib, Seaborn

4. Results & Insights
	• Top jihadist influencers were identified based on retweet counts, mentions, and tweet sentiment.
	• Suspicious users were flagged for monitoring based on their connections and interactions.
	• The best clustering model used Mahalanobis distance with 2 clusters (FPC = 0.85).

5. Future Enhancements
	• Deep Learning-based NLP models (like BERT) for better sentiment analysis.
	• Real-time anomaly detection to catch sudden activity spikes.
	• Extend the methodology to fake news detection, cybercrime tracking, or child exploitation detection.

6. Interview Questions
Basic Questions
	1. What was the main objective of your project?
	2. Why did you choose Twitter as the primary data source?
	3. What challenges did you face in collecting and processing data?
Big Data & Graph Theory
	4. How does Graph Theory help in social network analysis?
	5. What is Betweenness Centrality, and why is it useful in this project?
	6. How did you handle real-time streaming data from Twitter?
Machine Learning & Fuzzy Clustering
	7. Why did you use Fuzzy C-Means instead of K-Means?
	8. What is the difference between Mahalanobis & Euclidean distance?
	9. How did you validate the optimal number of clusters?
Security & Real-World Applications
	10. How can this project be extended to financial fraud detection?
	11. What are some ethical concerns when tracking users online?
How would you implement this system in a government security agency?

## License

This project is licensed under the MIT License - see the LICENSE file for details.
