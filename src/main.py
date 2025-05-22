import tweepy

# Set up Twitter API credentials
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

# Authenticate with the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)  # Set wait_on_rate_limit to avoid rate limiting issues

# Define the target user you want to analyze
target_user_screen_name = 'target_user'

# Collect tweets and user data
try:
    target_user = api.get_user(screen_name=target_user_screen_name)
    tweets = api.user_timeline(screen_name=target_user_screen_name, count=200, tweet_mode='extended')

    # Print user information
    print(f"User Name: {target_user.name}")
    print(f"User Screen Name: {target_user.screen_name}")
    print(f"User Followers Count: {target_user.followers_count}")
    print(f"User Description: {target_user.description}\n")

    # Print recent tweets
    print("Recent Tweets:")
    for i, tweet in enumerate(tweets, start=1):
        print(f"Tweet {i}: {tweet.full_text}\n")

except tweepy.TweepError as e:
    print(f"Error: {e}")