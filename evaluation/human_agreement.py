"""Compute agreement between human and LLM judge ratings.

Input CSV columns: human_overall,judge_overall. This intentionally makes the
human calibration dataset explicit and reproducible.
"""
from __future__ import annotations
import argparse
import pandas as pd
from scipy.stats import spearmanr

def main():
    p = argparse.ArgumentParser(); p.add_argument("csv"); a = p.parse_args()
    df = pd.read_csv(a.csv).dropna(subset=["human_overall", "judge_overall"])
    h, j = df.human_overall.astype(float), df.judge_overall.astype(float)
    print({"n": len(df), "within_1": float((abs(h-j) <= 1).mean()), "spearman": float(spearmanr(h,j).statistic)})
if __name__ == "__main__": main()
