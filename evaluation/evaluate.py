"""Evaluation harness for the golden set.

Golden CSV schema: text,gold_intent,should_escalate
The harness reports accuracy, macro-F1 and escalation confusion counts.
Reply quality is intentionally separated: an LLM judge must be calibrated
against human ratings rather than treated as ground truth.
"""
import argparse
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from src.taxonomy import rule_intent
from src.escalation import escalation_decision

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("golden")
    args = ap.parse_args()
    df = pd.read_csv(args.golden)
    pred = df.text.fillna("").map(rule_intent)
    esc = [escalation_decision(t, 1.0, i)[0] for t, i in zip(df.text.fillna(""), pred)]
    print({"n": len(df), "intent_accuracy": accuracy_score(df.gold_intent, pred), "intent_macro_f1": f1_score(df.gold_intent, pred, average="macro")})
    print("escalation_confusion_matrix [gold rows x predicted cols]")
    print(confusion_matrix(df.should_escalate.astype(bool), esc, labels=[False, True]))

if __name__ == "__main__":
    main()
