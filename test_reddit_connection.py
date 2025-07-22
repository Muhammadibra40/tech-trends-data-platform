import praw
from config.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

# Initialization of the Reddit client.
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Test: Fetching the 5 hottest posts.
try:
    for post in reddit.subreddit("python").hot(limit=6):
        print(f"{post.title} (score: {post.score})")
    print("Reddit API connection successful.")
except Exception as e:
    print("Failed to connect to Reddit API.")
    print("Error:", e)
