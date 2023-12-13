import re
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Define data preprocessing functions
def clean_tweet(tweet_text):
    # Remove URLs, mentions, and hashtags
    cleaned_text = re.sub(r'http\S+|@\w+|#\w+', '', tweet_text)
    return cleaned_text

def tokenize_and_normalize(text):
    # Tokenize and normalize text (e.g., lowercase)
    tokens = text.lower().split()
    return tokens

# Read Twitter data from CSV file
data = pd.read_csv('tweets_1.csv')

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
