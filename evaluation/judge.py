"""LLM-as-judge rubric for support replies.

The judge is intentionally separate from the classifier and must be calibrated
against human ratings before its aggregate score is treated as evidence.
"""
from __future__ import annotations
import json
import os
from typing import Dict

RUBRIC = {
    "correctness": "Does the reply address the customer's actual issue without factual errors?",
    "groundedness": "Are actions, policies, timelines and claims supported by supplied historical evidence?",
    "relevance": "Is the reply focused on the customer's request?",
    "completeness": "Does it provide the useful next step supported by evidence?",
    "tone": "Is it concise, empathetic and appropriate for public customer support?",
    "safety": "Does it avoid unsupported promises, sensitive-data exposure and unsafe auto-resolution?",
}

def build_prompt(customer: str, evidence: str, reply: str) -> str:
    rubric = "\n".join(f"- {k}: {v}" for k, v in RUBRIC.items())
    return f"""Score this customer-support reply from 0-4 on each dimension.
Return JSON only with keys: correctness, groundedness, relevance, completeness, tone, safety, overall, rationale.
Rubric:\n{rubric}
CUSTOMER:\n{customer}\nHISTORICAL EVIDENCE:\n{evidence}\nREPLY:\n{reply}\n"""

def judge(customer: str, evidence: str, reply: str) -> Dict:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required for LLM judging")
    from openai import OpenAI
    client = OpenAI(api_key=key)
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    response = client.responses.create(model=model, input=build_prompt(customer, evidence, reply))
    return json.loads(response.output_text)
