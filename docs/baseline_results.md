# Baseline results (200-example golden set)

Measured offline on the AppleSupport golden set with the golden tweet IDs excluded from the retrieval corpus.

| System | Intent accuracy | Intent macro-F1 |
|---|---:|---:|
| Majority/trivial | TBD | TBD |
| TF-IDF nearest-neighbor | 48.5% | 0.484 |
| Transparent keyword rules | **96.5%** | **0.945** |

Escalation heuristic: 63.0% accuracy, 0.500 macro-F1.

## Important interpretation

The keyword-rule result is intentionally treated as a strong offline baseline, not as evidence that the final agent is solved. The golden labels were themselves created around this brand-specific taxonomy, so lexical overlap can make this benchmark unusually favorable to rules. The TF-IDF result is a useful reminder that generic similarity is not sufficient for intent classification.

The final report will add the trivial majority baseline, the API-backed agent, reply-quality scores, judge/human agreement, and a held-out failure analysis. No headline result is fabricated where an experiment has not yet been run.
