# Hiver SDE Intern — AppleSupport AI Agent

## 1. Problem framing

The goal is a support-assistance system for AppleSupport-style public Twitter conversations. A useful system must do three things separately: identify the customer's intent, draft a response grounded in historical AppleSupport behavior, and decide whether automation is safe.

**Good** means high macro-F1 across intents, historically grounded replies, and conservative escalation on ambiguous/high-risk cases. The system is intentionally scoped to public-message triage and drafting. It does not perform account actions, issue refunds, access private DMs, or claim current Apple policy from historical tweets.

## 2. Data and brand selection

The primary dataset is Customer Support on Twitter (TWCS). AppleSupport was selected after comparing support-account volume and inspecting representative customer→brand response pairs. The pipeline reconstructs usable customer/support pairs and keeps evaluation examples separate from retrieval fitting.

## 3. System

The offline agent combines a compact brand-specific intent taxonomy, TF-IDF historical retrieval, a conservative escalation gate, and a grounded response drafter. When an API-backed model is configured, the same retrieved evidence can be supplied to an LLM with instructions not to invent policies, timelines, refunds, or account actions.

Escalation is intentionally asymmetric: potential fraud/security/legal issues, ambiguous requests, weak retrieval evidence, and very short messages are routed to a human.

## 4. Baselines and measured results

The evaluation harness uses a 200-example golden set. The current benchmark produced:

| System | Intent accuracy | Intent macro-F1 |
|---|---:|---:|
| TF-IDF nearest-neighbor | 48.5% | 0.484 |
| Keyword/rule baseline | 96.5% | 0.945 |

The escalation heuristic is evaluated separately because escalation is a safety decision rather than an intent-classification task.

These numbers are **not presented as production performance**. The rule baseline is especially strong because the taxonomy was derived from the same domain and the golden labels can contain lexical signals that the rules exploit.

## 5. What is misleading about my headline number?

A 96.5% intent-accuracy number would be misleading as a headline for the complete agent. First, the taxonomy is intentionally compact and domain-specific. Second, the rule baseline is lexically aligned with the labels. Third, classification accuracy does not measure reply correctness, grounding, or safe escalation. Finally, a false auto-handling decision can be much more costly than a false escalation. The safer headline is therefore a **set of independently reported metrics**, with false-auto-handle rate and grounded reply quality treated as first-class outcomes.

## 6. Reply-quality evaluation

Reply quality is assessed independently using a six-dimension LLM-as-judge rubric: correctness, groundedness, relevance, completeness, tone, and safety. Each dimension is scored 0–4. The judge is instructed to reward evidence-supported answers rather than fluent but unsupported answers.

Human calibration is a required gate before reporting judge agreement. The repository therefore includes the judge/calibration harness but does not fabricate a human-agreement statistic when a human-rated calibration file is absent.

## 7. Failure analysis

1. **Ambiguous messages.** Short messages such as “help” provide insufficient information. Hypothesis: intent needs confidence/abstention rather than forced classification.
2. **Multi-intent messages.** A single tweet can combine billing, device, and account problems. Hypothesis: allow multi-label intent or route to a human when several intents are detected.
3. **Missing precedent.** Historical retrieval can return superficially similar cases without a valid resolution. Hypothesis: add a calibrated retrieval threshold and contradiction checks.
4. **Overconfident drafting.** Reusing a historical answer can accidentally imply a current policy or promise. Hypothesis: extract only action patterns and require evidence for concrete claims.
5. **Unsafe automation.** A semantically clear message can still be high-risk. Hypothesis: maintain a separate risk policy rather than deriving escalation solely from intent confidence.

## 8. Next week

With one additional week I would (a) have two humans independently label the golden set and adjudicate disagreements, (b) add a stronger semantic retriever and evaluate retrieval recall, (c) run an API-backed grounded generator across the full benchmark, (d) calibrate an escalation threshold against an explicit cost matrix, and (e) add temporal evaluation so historical responses are not treated as current policy.

## 9. Reproducibility

The README documents the local setup and deterministic sampling. The raw TWCS CSV is intentionally excluded from git because it is large; the evaluator accepts a local `data/raw/twcs.csv`. Results should be regenerated rather than copied into the code.
