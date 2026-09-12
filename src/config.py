from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    brand: str = os.getenv("SUPPORT_BRAND", "AppleSupport")
    model: str = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    top_k: int = int(os.getenv("TOP_K", "5"))
    escalation_threshold: float = float(os.getenv("ESCALATION_THRESHOLD", "0.55"))

settings = Settings()
