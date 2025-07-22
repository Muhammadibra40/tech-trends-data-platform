CREATE TABLE IF NOT EXISTS reddit_posts (
    post_id        TEXT PRIMARY KEY,           
    subreddit      TEXT NOT NULL,
    title          TEXT NOT NULL,
    author         TEXT,
    score          INT,
    num_comments   INT,
    created_utc    TIMESTAMP,
    retrieved_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
