import praw
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
from config.config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    DB_URI,
)

SUBREDDITS = ["python", "dataengineering", "programming"]   # Wanted subreddits
POST_LIMIT = 50                                             # Posts per subreddit

def get_reddit_client():
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )

def extract(client):
    rows = []
    for sub in SUBREDDITS:
        for post in client.subreddit(sub).hot(limit=POST_LIMIT):
            rows.append(
                {
                    "post_id": post.fullname,   
                    "subreddit": sub,
                    "title": post.title,
                    "author": str(post.author) if post.author else None,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "created_utc": datetime.utcfromtimestamp(post.created_utc),
                }
            )
    return pd.DataFrame(rows)

def load(df: pd.DataFrame):
    engine = create_engine(DB_URI)
    with engine.begin() as conn:
        # Upsert – ignoring rows whose PK already exists
        df.to_sql("reddit_posts_temp", conn, if_exists="replace", index=False)
        conn.execute(
            text(
                """
                INSERT INTO reddit_posts
                SELECT * FROM reddit_posts_temp
                ON CONFLICT (post_id) DO NOTHING;
                DROP TABLE reddit_posts_temp;
                """
            )
        )

def run():
    reddit = get_reddit_client()
    df = extract(reddit)
    print(f"Fetched {len(df)} posts")
    load(df)
    print("Loaded into database successfully")

if __name__ == "__main__":
    run()
