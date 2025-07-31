
---

## ✅ 2. `HLD.md` – High Level Design

```markdown
# 📊 High-Level Design: Jihadist Detection System

## 🔧 Architecture Components

1. **Data Source**
   - Kaggle CSV
   - Twitter Streaming API

2. **Processing Engine**
   - Text cleaning
   - BERT-based sentiment score

3. **Graph Builder**
   - Mentions → NetworkX graph
   - Centrality score = Eigenvector, Closeness, Betweenness (Influence)

4. **Clustering Engine**
   - Fuzzy C-Means
   - Gustafson-Kessel for elliptical clusters

5. **Database**
   - MongoDB for storing classified users

6. **REST API**
   - FastAPI with GET /users/{risk}
   - POST /analyze_tweet

7. **Visualization**
   - Streamlit Dashboard

8. **Alerts**
   - Kafka consumer + SMTP

9. **Deployment**
   - Docker + Kubernetes YAMLs
