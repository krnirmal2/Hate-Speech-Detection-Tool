
---

# 📘 INTERVIEW DOCUMENTATION – JIHADIST DETECTION SYSTEM

---

## 1️⃣ **Project Overview (Elevator Pitch)**

> **“This project is a real-time AI-powered system that detects jihadist or extremist activity on Twitter. It uses BERT for sentiment analysis, graph theory to detect influencers, and fuzzy clustering to classify users into Low, Medium, or High risk. Results are stored in MongoDB and accessed through FastAPI. The system also includes a dashboard for visualization and Kafka-based alerts for real-time monitoring.”**

---

## 2️⃣ **Tech Stack**

| Layer           | Tools Used                          |
| --------------- | ----------------------------------- |
| Language        | Python 3.9                          |
| NLP             | BERT (`transformers`)               |
| Graph Analytics | NetworkX                            |
| Clustering      | Fuzzy C-Means (`skfuzzy`)           |
| Database        | MongoDB                             |
| Backend         | FastAPI                             |
| Streaming       | Apache Kafka                        |
| UI Dashboard    | Streamlit                           |
| Deployment      | Docker, Kubernetes (YAML + Compose) |

---

## 3️⃣ **Modules and Their Responsibilities**

### `data_loader.py`

* Loads tweets from CSV or Twitter API
* Removes bots, NaNs, and duplicate entries

### `text_preprocessing.py`

* Uses pretrained BERT (`nlptown`) to classify tweet sentiment (1–5 stars)
* Converts sentiment to score between -1 and +1

### `graph_analysis.py`

* Builds social graph from tweet mentions
* Computes centrality (Eigenvector, Betweenness, Degree)
* Detects root propagator (first influencer)

### `fuzzy_clustering.py`

* Uses `sentiment_score`, `eigenvector_centrality`, `followers_count`
* Applies **Fuzzy C-Means** and **Gustafson-Kessel** (adaptive clustering)
* Outputs:

  * Cluster center
  * Fuzzy Partition Coefficient (FPC)
  * Risk label: Low, Medium, High

### `database.py`

* Connects to MongoDB (`localhost:27017`)
* Saves and queries user data by risk level

### `api.py`

* FastAPI Endpoints:

  * `GET /users/{risk_category}`
  * `POST /analyze_tweet`

### `dashboard.py`

* Live Streamlit UI
* Shows:

  * Risk distribution
  * Top influencers
  * Recent classified tweets

### `alerts.py`

* Kafka consumer
* Sends SMTP email when extremist tweet count exceeds threshold in a time window

### `main.py`

* Integrates all steps:

  * Load → Sentiment → Graph → Clustering → MongoDB → Visualize

---

## 4️⃣ **Project Architecture Diagram (Talk-Through)**

```
              +--------------------+
              |  Twitter API / CSV |
              +--------------------+
                        ↓
              +--------------------+
              | Text Preprocessing |
              |  (BERT Sentiment)  |
              +--------------------+
                        ↓
              +--------------------+
              | Social Graph (NX)  |
              | Eigenvector Score  |
              +--------------------+
                        ↓
              +--------------------+
              | Fuzzy Clustering   |
              | FPC + Risk Label   |
              +--------------------+
                        ↓
         +-------------+-------------+
         | MongoDB                   |
         | FastAPI Backend           |
         | Streamlit Dashboard       |
         +-------------+-------------+
                        ↓
                 Kafka + SMTP Alerts
```

---

## 5️⃣ **Important Metrics and Algorithms**

| Metric/Method                    | Purpose                                     |
| -------------------------------- | ------------------------------------------- |
| **Sentiment Score (BERT)**       | Indicates radical tone of tweet             |
| **Eigenvector Centrality**       | Measures influence in network               |
| **FPC (Fuzzy Partition Coeff.)** | Validates clustering quality                |
| **Gustafson-Kessel**             | Allows elliptical cluster shapes (flexible) |

---

## 6️⃣ **Cluster Interpretation**

| Cluster Label | Traits                                     |
| ------------- | ------------------------------------------ |
| Low Risk      | Neutral sentiment, low influence           |
| Medium Risk   | Mixed sentiment, mid-level influence       |
| High Risk     | Radical tone, high followers, central user |

---

## 7️⃣ **Deployment Strategy**

* Dockerized services:

  * `api`, `dashboard`, `mongo`
* `docker-compose.yml` for local orchestration
* Kubernetes YAML for cloud-scale deployment (EKS, GKE)

---

## 8️⃣ **Security and Extensibility**

* OAuth2 for API (optional)
* Extendable to fake news detection
* Integration with law enforcement via secure dashboards

---

## 9️⃣ **Common Interview Questions**

### ➤ Architecture

* "How does your pipeline process and classify tweets?"
* "Why did you choose fuzzy clustering over hard clustering (like KMeans)?"
* "What’s the role of eigenvector centrality in your analysis?"

### ➤ NLP

* "Why use BERT over VADER for sentiment?"
* "How do you handle multilingual tweets?"

### ➤ Clustering

* "How do you evaluate cluster quality?" → FPC
* "What if a user belongs to multiple clusters equally?" → fuzzy logic

### ➤ Deployment

* "How would you scale this to millions of tweets?" → Kafka + Kubernetes
* "What failure recovery strategy would you use for real-time streaming?"

---

## 🔟 Final Advice for Interview

* Be ready to **draw the architecture** on a whiteboard
* Emphasize:

  * Real-time alerting
  * Fuzzy logic for nuanced classification
  * BERT for high NLP accuracy
* Show screenshots (Streamlit, clustering visualization)
* Suggest **future work**:

  * Deep learning classifiers
  * Government data integration
  * Use of Neo4j for graph DB

---

