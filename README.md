# 🚨 Jihadist Detection System

This system detects jihadist/extremist activity on Twitter using advanced AI, graph theory, and fuzzy clustering techniques.

### Distinguishing Dangerous Users
The system employs Gustafson-Kessel fuzzy clustering to categorize users. This clustering process groups users based on their textual content and social graph interactions, allowing for the identification of potential "dangerous users" who may be spreading harmful or malicious content. The classified users are then saved to MongoDB for further analysis and monitoring.

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



## Clone repo
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

## 1. How to Install

```bash
pip install -r requirements.txt

# Install code formatter
pip install black
```

## 2. Code Formatting

Format all Python files using Black:
```bash
black .
```

Format specific directory:
```bash
black src/
```

## 2. 🚀 How to Run

### 1. Main Analysis Pipeline
```bash
python src/service/main.py
```

### 2. Dashboard result from database after running main pipeline
```bash
streamlit run src/dashboard/dashboard.py
```

### 3. API Endpoints
```bash
# Start API
python src/controller/api.py

# Test detection endpoint
curl -X POST -H "Content-Type: application/json" -d @data/test.json http://localhost:5000/api/detect
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
│   ├── config/             # Configuration files
│   │   └── config.py
│   ├── controller/         # FastAPI endpoints
│   │   └── api.py
│   ├── dashboard/          # Streamlit dashboard
│   │   └── dashboard.py
│   ├── data/               # Data directory
│   │   └── twitter_sentiment_analysis.csv
│   ├── kafka/              # Kafka producers and consumers
│   │   ├── kafka_consumer.py
│   │   └── kafka_producer.py
│   ├── logs/               # Logging and monitoring
│   │   ├── alerts.py
│   │   ├── logger.py
│   │   └── monitoring.py
│   ├── models/             # Model files
│   ├── repository/         # Database operations
│   │   └── database.py
│   ├── service/            # Core business logic
│   │   ├── clusteringStrategy/ # Fuzzy Clustering implementations
│   │   │   └── fuzzy_clustering.py
│   │   ├── data_loader.py  # Data loading and cleaning
│   │   ├── graph_analysis.py # NetworkX social graph logic
│   │   ├── main.py         # Main pipeline script
│   │   ├── stream_processor.py # Kafka stream processing
│   │   └── text_preprocessing.py # BERT sentiment analysis
├── deployment/             # Docker and Kubernetes deployment files
├── oldCode/                # Older code versions
├── tests/                  # Test suite
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


## License
This project is licensed under the MIT License - see the LICENSE file for details.
