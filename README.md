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
