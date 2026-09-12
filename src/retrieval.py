"""Lightweight lexical retrieval baseline; no vector DB required."""
from dataclasses import dataclass
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class Case:
    customer_text: str
    response_text: str
    score: float

class TfidfRetriever:
    def __init__(self, cases: pd.DataFrame):
        self.cases = cases.reset_index(drop=True)
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2), min_df=2, max_features=100_000)
        self.matrix = self.vectorizer.fit_transform(self.cases.customer_text.fillna(""))

    def search(self, query: str, k: int = 5):
        q = self.vectorizer.transform([query or ""])
        scores = cosine_similarity(q, self.matrix).ravel()
        idx = scores.argsort()[::-1][:k]
        return [Case(self.cases.iloc[i].customer_text, self.cases.iloc[i].response_text, float(scores[i])) for i in idx]


def clean_text(text: str) -> str:
    text = re.sub(r"https?://\S+", "", text or "")
    text = re.sub(r"@\w+", "", text)
    return re.sub(r"\s+", " ", text).strip()
