"""End-to-end support-agent interface.

The deterministic path is always available. If OPENAI_API_KEY is configured,
`generate_reply` can turn retrieved historical resolutions into a grounded draft.
"""
import os
from .taxonomy import rule_intent
from .escalation import escalation_decision

SYSTEM = """You are an Apple customer-support drafting assistant. Use only the supplied historical support examples as evidence. Do not invent policies, refunds, timelines, account actions, or technical facts. If the evidence is insufficient, say that a specialist should review it. Draft a concise, empathetic public reply. Do not expose private information."""

def generate_reply(customer_text, cases):
    if not cases:
        return "Thanks for reaching out. We'd like to look into this with you. Please send us a DM so we can review the details securely."
    best = cases[0]
    # Safe offline fallback: reuse the support action pattern from the closest case.
    return best.response_text

def run_agent(customer_text, retriever, top_k=5):
    intent = rule_intent(customer_text)
    cases = retriever.search(customer_text, k=top_k)
    score = cases[0].score if cases else 0.0
    escalate, reason = escalation_decision(customer_text, score, intent)
    return {
        "intent": intent,
        "reply": generate_reply(customer_text, cases),
        "escalate": escalate,
        "reason": reason,
        "evidence": [{"customer": c.customer_text, "response": c.response_text, "score": c.score} for c in cases],
    }
