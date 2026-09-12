"""Utilities for reconstructing customer/support relationships."""
import pandas as pd

def build_pairs(df, brand="AppleSupport"):
    by_id = df.set_index("tweet_id")
    support = df[(df["author_id"] == brand) & (~df["inbound"])].copy()
    rows=[]
    for r in support.itertuples():
        if pd.isna(r.in_response_to_tweet_id): continue
        try: parent=by_id.loc[int(r.in_response_to_tweet_id)]
        except (KeyError, ValueError, TypeError): continue
        if bool(parent.inbound):
            rows.append({"customer_tweet_id":int(parent.tweet_id),"support_tweet_id":int(r.tweet_id),"customer_text":parent.text,"support_text":r.text})
    return pd.DataFrame(rows)
