## Low-Level Design

# 🧠 Low-Level Design: Jihadist Detection System

---

## 📁 Module Descriptions

### `data_loader.py`
- Loads tweet dataset
- Drops nulls, bots, duplicates

### `text_preprocessing.py`
- Uses `nlptown/bert-base-multilingual-uncased-sentiment`
- Converts label → numeric sentiment

### `graph_analysis.py`
- NetworkX Graph
- Computes:
  - Eigenvector centrality
  - Closeness centrality
  - Betweenness centrality
  - Finds root propagator

### `src/service/clusteringStrategy/fuzzy_clustering.py`
- Normalizes features:
  - Sentiment
  - Centrality
  - Followers
- Uses `skfuzzy` C-Means
- Calculates FPC
- Maps clusters → "High", "Medium", "Low Risk"

### `src/repository/database.py`
- Connects to MongoDB
- Saves and queries user profiles

### `src/controller/api.py`
- FastAPI
- Endpoints:
  - GET /users/{risk_category}
  - POST /analyze_tweet

### `src/dashboard/dashboard.py`
- Streamlit
- Plots:
  - Risk category distribution
  - Influencers
  - Recent tweets

### `src/logs/alerts.py`
- Kafka consumer
- Email alert if high-risk tweet volume > threshold

### `src/service/main.py`
- Pipeline runner:
  - Load → Sentiment → Graph → Clustering → DB
