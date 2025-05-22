# Real-time alerting logic
# ✅ 8. alerts/alerts.py
# 📄 Purpose:
# Consume tweets from Kafka topic (twitter_stream)

# Detect spikes in high-risk classified tweets

# Trigger an email alert if threshold exceeded
# alerts/alerts.py

from kafka import KafkaConsumer
import json
import smtplib
import time

# Alert Configuration
THRESHOLD = 5        # Number of high-risk tweets
TIME_WINDOW = 60     # Seconds
EMAIL_FROM = "your_email@gmail.com"
EMAIL_TO = "security_team@example.com"
EMAIL_PASSWORD = "your_app_password"  # Use app password if using Gmail

# SMTP Setup
def send_email_alert(message: str):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)

        subject = "🚨 Extremist Activity Alert!"
        msg = f"Subject: {subject}\n\n{message}"

        server.sendmail(EMAIL_FROM, EMAIL_TO, msg)
        server.quit()
        print("✅ Alert email sent.")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")

# Kafka Consumer Setup
consumer = KafkaConsumer(
    'twitter_stream',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Monitoring Loop
high_risk_counter = 0
start_time = time.time()

print("📡 Monitoring high-risk tweet activity...")

for msg in consumer:
    tweet = msg.value
    risk = tweet.get("risk_category", "Unknown")

    if risk == "High Risk":
        high_risk_counter += 1
        print(f"⚠️ High-risk tweet detected: {tweet['username']}")

    # Check time window
    if time.time() - start_time >= TIME_WINDOW:
        if high_risk_counter >= THRESHOLD:
            send_email_alert(f"{high_risk_counter} high-risk tweets detected in {TIME_WINDOW} seconds!")
        # Reset counters
        high_risk_counter = 0
        start_time = time.time()

        
# | Component            | Description                            |
# | -------------------- | -------------------------------------- |
# | `KafkaConsumer`      | Listens to topic with real-time tweets |
# | `risk_category`      | Checked for "High Risk" tags           |
# | `send_email_alert()` | Sends email if threshold exceeded      |
