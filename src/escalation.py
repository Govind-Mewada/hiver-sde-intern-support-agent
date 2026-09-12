"""Conservative safety gate for auto-handling."""
import re

HIGH_RISK = [
    r"fraud", r"scam", r"stolen", r"hack", r"hacked", r"unauthorized",
    r"legal", r"lawsuit", r"lawyer", r"chargeback", r"identity theft",
    r"suicide", r"self[- ]harm", r"threat", r"police",
]

AMBIGUITY = [r"help", r"please help", r"what do i do", r"not working", r"issue", r"problem"]

def escalation_decision(text: str, retrieval_score: float = 0.0, intent: str = "general_support"):
    t = (text or "").lower()
    for pat in HIGH_RISK:
        if re.search(pat, t):
            return True, f"high-risk signal: {pat}"
    if intent == "general_support" or retrieval_score < 0.12:
        return True, "insufficient evidence for a safe automated resolution"
    if len(t.split()) < 4:
        return True, "message is too short/ambiguous"
    return False, "clear intent and sufficiently similar historical support case"
