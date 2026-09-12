"""Streaming-friendly preprocessing for TWCS."""
import pandas as pd

REQUIRED_COLUMNS = ["tweet_id","author_id","inbound","created_at","text","response_tweet_id","in_response_to_tweet_id"]

def read_twcs(path, chunksize=100_000):
    return pd.read_csv(path, usecols=REQUIRED_COLUMNS, chunksize=chunksize)

def normalize_text(text):
    if pd.isna(text): return ""
    return " ".join(str(text).split())
