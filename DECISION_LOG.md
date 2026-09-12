# Decision log

1. **Selected AppleSupport.** It has substantial support-account volume and many reconstructable customer→brand response pairs.
2. **Use a brand-specific taxonomy.** The assignment asks for intents defined from the chosen data; a generic 77-class banking taxonomy would not reflect AppleSupport behavior.
3. **Keep the taxonomy compact.** Fewer, well-supported intents are easier to evaluate reliably than dozens of sparse labels.
4. **Treat historical replies as evidence, not policy.** Public tweets can be stale, so the agent must not claim that a historical action is currently guaranteed.
5. **Separate retrieval from generation.** This makes evidence inspectable and lets the same retrieval baseline be compared with the full agent.
6. **Use TF-IDF as the simple baseline.** It is transparent, fast, deterministic, and establishes whether semantic machinery adds value.
7. **Include a majority/keyword baseline.** A strong trivial/simple benchmark prevents an impressive-looking model from hiding an easy label shortcut.
8. **Optimize for macro-F1, not only accuracy.** Intent distributions are imbalanced and rare intents matter.
9. **Make escalation asymmetric.** Missing evidence and high-risk signals should favor a human over speculative automation.
10. **Keep evaluation data out of retrieval fitting.** Otherwise the benchmark can leak exact historical examples and inflate performance.
11. **Separate reply quality from intent quality.** Correct classification does not imply a correct or grounded response.
12. **Use an LLM judge only after calibration.** Judge scores are measurements, not ground truth; human agreement must be checked.
13. **Do not fabricate human agreement.** If human calibration labels are missing, report the limitation rather than inventing correlation/agreement.
14. **Exclude the raw dataset from git.** The source CSV is hundreds of MB; reproducibility instructions point to a local copy instead.
15. **Do not build account-action tooling.** The take-home is about triage/drafting and historical grounding, not production access to customer accounts.
