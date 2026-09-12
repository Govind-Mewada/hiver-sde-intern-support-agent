"""Build the golden evaluation CSV from the TWCS raw CSV and committed labels.

Usage:
    python scripts/build_golden.py --data /path/to/twcs.csv
"""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd

REQUIRED = ["tweet_id", "created_at", "text", "author_id", "inbound", "response_tweet_id"]

def parse_id_list(value):
    if pd.isna(value):
        return []
    out=[]
    for part in str(value).split(","):
        try: out.append(int(float(part)))
        except ValueError: pass
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--labels", default="data/golden_labels.csv")
    ap.add_argument("--output", default="data/golden_set.csv")
    args=ap.parse_args()
    labels=pd.read_csv(args.labels)
    ids=set(labels.tweet_id.astype(int))
    replies={}
    chunks=[]
    for chunk in pd.read_csv(args.data, usecols=REQUIRED, chunksize=250_000):
        if (chunk.author_id == "AppleSupport").any():
            a=chunk[chunk.author_id == "AppleSupport"]
            for _,r in a.iterrows():
                replies[int(r.tweet_id)] = r.text
        hit=chunk[chunk.tweet_id.isin(ids)]
        if len(hit): chunks.append(hit)
    tweets=pd.concat(chunks, ignore_index=True).drop_duplicates("tweet_id")
    tweets["evidence_response"] = tweets.response_tweet_id.map(
        lambda v: next((replies[i] for i in parse_id_list(v) if i in replies), "")
    )
    out=labels.merge(tweets[["tweet_id","created_at","text","evidence_response"]], on="tweet_id", how="left")
    out=out.rename(columns={"text":"customer_text"})
    out["label_source"]="analyst_review_v2"
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output,index=False)
    print(f"wrote {len(out)} examples -> {args.output}")

if __name__ == "__main__": main()
