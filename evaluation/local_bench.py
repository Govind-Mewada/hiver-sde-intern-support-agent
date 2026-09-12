"""Offline benchmark runner used to produce the committed baseline metrics.

It intentionally excludes golden-set tweet IDs from the retrieval corpus.
Run from the repository root:
    python evaluation/local_bench.py data/raw/twcs.csv data/golden_set.csv
"""
from __future__ import annotations
import argparse, json, re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.neighbors import NearestNeighbors
from src.taxonomy import rule_intent

ESC_RE = re.compile(r"\b(refund|charged|charge|fraud|hacked|stolen|lost|deleted|missing|locked|disabled|security|scam|unauthorized|credit card|account)\b|\bphotos?\b.*\b(deleted|lost|missing)\b", re.I)

def main(raw_path: str, gold_path: str) -> None:
    gold = pd.read_csv(gold_path).fillna("")
    raw = pd.read_csv(raw_path, usecols=["tweet_id","author_id","inbound","text","in_response_to_tweet_id"])
    support = raw[(raw.author_id == "AppleSupport") & (~raw.inbound)]
    customer = raw[raw.inbound]
    pairs = support.merge(customer[["tweet_id","text"]], left_on="in_response_to_tweet_id", right_on="tweet_id", suffixes=("_support","_customer"))
    train = pairs[~pairs.tweet_id_customer.isin(set(gold.tweet_id))].copy()
    train["label"] = train.text_customer.map(rule_intent)
    train = train[train.label != "general_support"]
    if len(train) > 50000:
        train = train.sample(50000, random_state=42)

    rule_pred = gold.customer_text.map(rule_intent)
    vec = TfidfVectorizer(ngram_range=(1,2), min_df=2, max_features=120000, sublinear_tf=True)
    X = vec.fit_transform(train.text_customer.astype(str))
    knn = NearestNeighbors(n_neighbors=5, metric="cosine", n_jobs=-1).fit(X)
    distances, indices = knn.kneighbors(vec.transform(gold.customer_text.astype(str)))
    nn_pred = []
    for inds, ds in zip(indices, distances):
        scores = {}
        for i, d in zip(inds, ds):
            label = train.iloc[i].label
            scores[label] = scores.get(label, 0) + 1 / (d + 1e-3)
        nn_pred.append(max(scores, key=scores.get))

    esc_pred = gold.customer_text.map(lambda x: int(bool(ESC_RE.search(x))))
    summary = {
        "n": len(gold),
        "rule_accuracy": float(accuracy_score(gold.intent, rule_pred)),
        "rule_macro_f1": float(f1_score(gold.intent, rule_pred, average="macro")),
        "tfidf_nn_accuracy": float(accuracy_score(gold.intent, nn_pred)),
        "tfidf_nn_macro_f1": float(f1_score(gold.intent, nn_pred, average="macro")),
        "escalation_heuristic_accuracy": float(accuracy_score(gold.escalate_label, esc_pred)),
        "escalation_heuristic_macro_f1": float(f1_score(gold.escalate_label, esc_pred, average="macro")),
        "retrieval_train_pairs": int(len(train)),
    }
    with open("evaluation/results.json", "w") as f:
        json.dump(summary, f, indent=2)
    out = gold[["tweet_id","intent","escalate_label"]].copy()
    out["rule_pred"] = rule_pred
    out["tfidf_nn_pred"] = nn_pred
    out["escalation_pred"] = esc_pred
    out.to_csv("evaluation/predictions.csv", index=False)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("raw_path")
    p.add_argument("gold_path")
    a = p.parse_args()
    main(a.raw_path, a.gold_path)
