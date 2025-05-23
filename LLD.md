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
  - Finds root propagator

### `fuzzy_clustering.py`
- Normalizes features:
  - Sentiment
  - Centrality
  - Followers
- Uses `skfuzzy` C-Means
- Calculates FPC
- Maps clusters → "High", "Medium", "Low Risk"

### `database.py`
- Connects to MongoDB
- Saves and queries user profiles

### `api.py`
- FastAPI
- Endpoints:
  - GET /users/{risk_category}
  - POST /analyze_tweet

### `dashboard.py`
- Streamlit
- Plots:
  - Risk category distribution
  - Influencers
  - Recent tweets

### `alerts.py`
- Kafka consumer
- Email alert if high-risk tweet volume > threshold

### `main.py`
- Pipeline runner:
  - Load → Sentiment → Graph → Clustering → DB
