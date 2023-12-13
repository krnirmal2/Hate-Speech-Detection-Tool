import pandas as pd
from textblob import TextBlob
import re
import nltk
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
import skfuzzy as fuzz
import networkx as nx
import matplotlib.pyplot as plt




# Download the VADER lexicon (required for SentimentIntensityAnalyzer)
nltk.download('vader_lexicon')

# Initialize SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Read Twitter data from CSV file (assuming 'twitter_data.csv' has a 'Tweet' column)
data = pd.read_csv('tweets_1.csv')

# Define data preprocessing functions (you can reuse your existing functions)
def clean_tweet(tweet_text):
    # Remove URLs, mentions, and hashtags
    cleaned_text = re.sub(r'http\S+|@\w+|#\w+', '', tweet_text)
    return cleaned_text

def tokenize_and_normalize(text):
    # Tokenize and normalize text (e.g., lowercase)
    tokens = text.lower().split()
    return tokens

# Preprocess tweet text from the CSV
data['Cleaned_Tweet'] = data['tweets'].apply(clean_tweet)
data['Tokenized_Tweet'] = data['Cleaned_Tweet'].apply(tokenize_and_normalize)



# Build a simple user graph
user_graph = nx.DiGraph()

# Add the target user as a node (replace 'target_user_screen_name' with the actual target user)
target_user_screen_name = 'YazeedDhardaa25'
user_graph.add_node(target_user_screen_name)

# Add followers as nodes and edges
for follower_id in data['username']:
    try:
        # Add follower as a node
        user_graph.add_node(follower_id)
        
        # Add edge from follower to target user
        user_graph.add_edge(follower_id, target_user_screen_name)
    except:
        # Handle errors when adding nodes or edges
        pass

# Visualize the user graph
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(user_graph, seed=42)
nx.draw(user_graph, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=10)
plt.title("Twitter User Graph")
plt.show()







# Analyze sentiment of each tweet
sentiment_scores = [sia.polarity_scores(tweet) for tweet in data['Cleaned_Tweet']]

# Categorize tweets as positive, negative, or neutral based on sentiment scores
sentiment_categories = []
for score in sentiment_scores:
    if score['compound'] >= 0.05:
        sentiment_categories.append('positive')
    elif score['compound'] <= -0.05:
        sentiment_categories.append('negative')
    else:
        sentiment_categories.append('neutral')

# Display sentiment analysis results for the first few tweets
for i, (tweet, sentiment) in enumerate(zip(data['Cleaned_Tweet'][:5], sentiment_categories[:5]), start=1):
    print(f"Tweet {i}:")
    print(f"Text: {tweet}")
    print(f"Sentiment: {sentiment}")
    print(f"Sentiment Scores: {sentiment_scores[i - 1]}\n")



# Extract the sentiment compound scores as a feature
sentiment_features = np.array([score['compound'] for score in sentiment_scores]).reshape(-1, 1)

# Define the number of clusters
n_clusters = 2

# Define the maximum number of iterations for the clustering algorithm
max_iterations = 100

# Initialize cluster centers using K-means
cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    sentiment_features.T, n_clusters, 2, error=0.005, maxiter=max_iterations)

# Calculate the cluster memberships for each data point
cluster_membership = np.argmax(u, axis=0)

# Count the number of data points in each cluster
cluster_counts = np.bincount(cluster_membership)

# Define a threshold for considering a cluster as potentially containing hate speech
hate_speech_threshold = 0.6  # Adjust as needed

# Identify clusters with a high proportion of negative sentiment
hate_speech_clusters = []
for i, count in enumerate(cluster_counts):
    if count > 0:
        cluster_sentiment_scores = [sentiment_scores[j]['compound'] for j in range(len(data)) if cluster_membership[j] == i]
        negative_count = sum(1 for score in cluster_sentiment_scores if score < -0.05)
        if (negative_count / count) > hate_speech_threshold:
            hate_speech_clusters.append(i)


# Display tweets in the identified hate speech clusters
for cluster_index in hate_speech_clusters:
    print(f"Hate Speech Cluster {cluster_index}:")
    cluster_tweets = [data['Cleaned_Tweet'][i] for i, cluster in enumerate(cluster_membership) if cluster == cluster_index]
    for tweet in cluster_tweets:
        pass
        # print(f"Text: {tweet}\n")




# Create a directed graph
G = nx.DiGraph()

# Add nodes for each user
users = data['username'].unique()  # Assuming 'User' is the user identifier in your dataset
G.add_nodes_from(users)

# Add directed edges based on interactions (you may need to adapt this based on your data)
for i, row in data.iterrows():
    source_user = row['username']
    mentioned_users = re.findall(r'@\w+', row['tweets'])  # Extract mentioned users
    for mentioned_user in mentioned_users:
        G.add_edge(source_user, mentioned_user)


# Calculate degree centrality for each node (a simple measure)
degree_centrality = nx.degree_centrality(G)

# Calculate betweenness centrality for each node (identifies users in control of information flow)
betweenness_centrality = nx.betweenness_centrality(G)

# Calculate eigenvector centrality for each node (identifies influential users)
eigenvector_centrality = nx.eigenvector_centrality(G)

# Define a threshold for identifying central users (adjust as needed)
centrality_threshold = 0.1

# Find the user with the highest centrality score (e.g., degree centrality)
most_central_user = max(degree_centrality, key=degree_centrality.get)

# Check if the most central user's centrality score exceeds the threshold
if degree_centrality[most_central_user] > centrality_threshold:
    print(f"The most central user who has spread hate speech is: {most_central_user}")
else:
    print("No central user found who has spread hate speech.")


# Create a layout for the graph
pos = nx.spring_layout(G)

# Draw the graph
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000)

# Highlight the most central user in red
nx.draw_networkx_nodes(G, pos, nodelist=[most_central_user], node_color='red', node_size=3000)

# Label the most central user
labels = {most_central_user: most_central_user}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='black')

plt.title("User Interaction Network")
plt.axis('off')
plt.show()
