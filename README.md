# Hiver SDE Intern — Customer Support AI Agent

A reproducible support-agent prototype built from the Customer Support on Twitter (TWCS) dataset. The selected brand is **AppleSupport**, chosen after profiling support-account volume and inspecting representative customer→brand response pairs.

## What it does

1. Classifies an incoming customer tweet into a compact AppleSupport-specific intent taxonomy.
2. Retrieves historically similar AppleSupport cases and their support responses.
3. Drafts a response grounded in those historical patterns.
4. Applies a conservative escalation gate with an explicit reason.

The project deliberately does **not** attempt private-DM resolution, account actions, refunds, or real-time Apple policy lookup. Public Twitter data is evidence of historical behavior, not a current policy source.

## Dataset

Use the Kaggle **Customer Support on Twitter** dataset (`thoughtvector/customer-support-on-twitter`). The raw CSV is intentionally not committed because it is ~500 MB. Put it at `data/raw/twcs.csv`.

## Quickstart

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python - <<'PY'
from src.preprocess import build_brand_pairs
n = build_brand_pairs('data/raw/twcs.csv', 'AppleSupport', 'data/brand_pairs.csv')
print('paired cases:', n)
PY
```

Then run the evaluation harness:

```bash
python -m evaluation.evaluate data/golden_set.csv
```

For API-backed generation, set `OPENAI_API_KEY` and `OPENAI_MODEL` in `.env`. The offline retrieval/rules path remains runnable without an API key.

## Evaluation philosophy

The primary metric is not a single chatbot score. We separately measure intent macro-F1, per-intent performance, escalation false-auto-handle rate, and grounded reply quality. Reply quality is judged with a six-dimension rubric and calibrated against human ratings on a held-out subset.

### Baselines

- **Trivial:** majority intent + generic support response.
- **Simple:** TF-IDF nearest-neighbor retrieval + transparent keyword intent rules.
- **Agent:** intent + historical retrieval + grounded response generation + escalation gate.

## Golden set

The golden set is sampled from held-out AppleSupport customer messages with deterministic random seeds. Sampling is stratified across intents and includes ambiguous/high-risk cases. Each example contains a human-reviewed intent, escalation label, and reply-quality criteria. No golden example is used to fit the retrieval index.

## Failure analysis

The report tracks five recurring risks: ambiguous messages, multi-intent messages, missing historical precedent, overconfident unsupported replies, and unsafe auto-handling.

## Reproducibility

All sampling uses explicit random seeds. Raw data is excluded from git; only derived, non-sensitive evaluation artifacts are committed. Final measured results will be frozen after the golden set and benchmark run are complete.
