"""Deterministic baselines used by the evaluation harness."""
from __future__ import annotations
import re
from collections import Counter
from src.taxonomy import rule_intent

INTENTS = [
    "device_update_problem", "battery_power", "account_access", "icloud",
    "app_store_itunes", "billing_charge", "apple_pay", "connectivity",
    "device_hardware", "order_delivery", "software_app", "general_support",
]

def majority_baseline(train_intents):
    majority = Counter(train_intents).most_common(1)[0][0]
    return lambda text: majority

def rule_baseline(text):
    return rule_intent(text)

def retrieval_similarity(query, cases, top_k=1):
    """Tiny TF-IDF-free lexical retrieval baseline; no external model required."""
    q=set(re.findall(r"[a-z0-9]+", query.lower()))
    scored=[]
    for c in cases:
        toks=set(re.findall(r"[a-z0-9]+", str(c["customer_text"]).lower()))
        score=len(q & toks) / max(1, len(q | toks))
        scored.append((score,c))
    scored.sort(key=lambda z:z[0], reverse=True)
    return scored[:top_k]
