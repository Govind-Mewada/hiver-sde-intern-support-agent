# Hiver SDE Intern — AI Support Agent

A reproducible take-home implementation for the Hiver SDE Intern assignment.

## Goal

Build and evaluate an AI customer-support agent for one brand from the Customer Support on Twitter dataset. The agent will:

1. Classify incoming customer messages into a small, data-derived intent taxonomy.
2. Draft a response grounded in historically resolved conversations.
3. Decide whether to auto-handle or escalate, with a reason.

## Evaluation-first design

This repository treats evaluation as the primary product. Results will include:

- Intent accuracy and macro-F1, including per-intent results.
- Reply-quality evaluation with an explicit rubric.
- LLM-as-judge validation against a human-scored subset.
- Escalation precision/recall and false-auto-handle analysis.
- Comparisons against a trivial baseline and a simple retrieval baseline.
- Failure analysis and a mandatory discussion of what the headline number hides.

## Reproduction

The final README will contain the exact commands, dataset access instructions, model configuration, and expected runtime needed to reproduce the headline results in under 15 minutes on a normal laptop/API setup.

## Project status

Initial repository scaffold created. Data profiling and brand selection are next; the brand and intent taxonomy are intentionally not hard-coded until the dataset is inspected.

## Structure

```text
.
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   ├── README.md
│   └── golden_set.csv
├── src/
│   ├── preprocessing.py
│   ├── conversation_builder.py
│   ├── taxonomy.py
│   ├── retrieval.py
│   ├── classifier.py
│   ├── responder.py
│   ├── escalation.py
│   └── pipeline.py
├── evaluation/
│   ├── evaluate.py
│   ├── metrics.py
│   ├── judge.py
│   ├── human_judge_agreement.py
│   └── baselines.py
├── experiments/
│   └── results.csv
├── notebooks/
│   └── exploration.ipynb
└── report/
    ├── report.md
    └── decision_log.md
```

## License

This project is an interview take-home implementation. Dataset terms and API/model terms remain those of their respective providers.
