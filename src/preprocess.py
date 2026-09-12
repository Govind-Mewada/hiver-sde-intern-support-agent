"""Streaming preprocessing for the 2.8M-row TWCS CSV."""
from pathlib import Path
import pandas as pd

COLS = ["tweet_id", "author_id", "inbound", "created_at", "text", "response_tweet_id", "in_response_to_tweet_id"]

def build_brand_pairs(csv_path: str, brand: str = "AppleSupport", out_path: str = "data/brand_pairs.csv", chunksize: int = 200_000) -> int:
    """Extract inbound tweets and their directly linked brand responses.

    The full dataset is never loaded into memory. Only rows authored by the
    selected support account or tweets explicitly addressing that account are kept.
    """
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    response_map = {}
    inbound_rows = []
    first = True
    written = 0

    # First pass: collect brand responses. Second pass: collect inbound tweets.
    for chunk in pd.read_csv(csv_path, usecols=COLS, chunksize=chunksize):
        for _, r in chunk[chunk.author_id == brand].iterrows():
            response_map[int(r.tweet_id)] = str(r.text or "")

    for chunk in pd.read_csv(csv_path, usecols=COLS, chunksize=chunksize):
        x = chunk[(chunk.inbound == True) & chunk.text.fillna("").str.contains("@" + brand, case=False, regex=False)].copy()
        rows = []
        for _, r in x.iterrows():
            rid = r.response_tweet_id
            if pd.isna(rid):
                continue
            for token in str(rid).split(","):
                try:
                    sid = int(float(token))
                except ValueError:
                    continue
                if sid in response_map:
                    rows.append({
                        "customer_tweet_id": int(r.tweet_id),
                        "customer_text": str(r.text or ""),
                        "response_tweet_id": sid,
                        "response_text": response_map[sid],
                        "created_at": r.created_at,
                    })
        if rows:
            pd.DataFrame(rows).to_csv(out_path, mode="w" if first else "a", header=first, index=False)
            first = False
            written += len(rows)
    return written
