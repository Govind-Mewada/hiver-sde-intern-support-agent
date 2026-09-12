"""AppleSupport intent taxonomy and transparent offline baseline classifier."""
from __future__ import annotations
import re

INTENTS = {
    "device_update_problem": "an iOS/macOS update or upgrade caused a device/software problem",
    "battery_power": "battery life, charging, overheating, or power issue",
    "account_access": "Apple ID, password, verification, lockout, sign-in, or account recovery",
    "icloud": "iCloud storage, sync, backup, or iCloud library/access issue",
    "app_store_itunes": "App Store, iTunes, Apple Music download, or app purchase/download issue",
    "billing_charge": "unexpected charge, declined payment, refund, billing, or payment dispute",
    "apple_pay": "Apple Pay / Apple Pay Cash / Wallet issue",
    "connectivity": "Wi-Fi, cellular/LTE, Bluetooth, hotspot, network, or internet issue",
    "device_hardware": "physical hardware, screen, camera, speaker, button, keyboard, or power-on issue",
    "order_delivery": "device order, preorder, reservation, pickup, shipping, tracking, or delivery issue",
    "software_app": "software/app crash, bug, error, freeze, slowness, or behavior issue not better covered elsewhere",
    "general_support": "ambiguous request, acknowledgement, or issue without enough evidence for another intent",
}

PATTERNS = [
    ("apple_pay", r"apple\s*pay|apple pay cash|\bwallet\b"),
    ("icloud", r"\bicloud\b|i cloud|icloud library|icloud backup"),
    ("order_delivery", r"\b(order|pre[- ]?order|shipping|shipment|reservation confirmation|reserve.*iphone|pickup.*store|delivery)\b"),
    ("battery_power", r"battery|battery life|charging|charger|overheat|overheating|power drain|power consumption"),
    ("billing_charge", r"\b(charged|billing|refund|refunded|payment method|payment|invoice|credit card|purchase dispute)\b"),
    ("account_access", r"apple id|password|locked out|account locked|verification code|security questions|sign[ -]?in|login|recover.*account|account.*recover|hacked"),
    ("app_store_itunes", r"app store|itunes|download.*app|app.*download|in[- ]app purchase|apple music.*download"),
    ("connectivity", r"wi[ -]?fi|bluetooth|cellular|lte|network|internet|signal|hotspot|connect.*wifi|connect.*car"),
    ("device_update_problem", r"\bios\s*\d|software update|\bupdated?\b|\bupgrade(d)?\b|latest (ios|software) update|after (the )?(latest )?(ios|software) update"),
    ("device_hardware", r"screen|display|cracked|broken|speaker|microphone|home button|keyboard|camera|hardware|won.t turn on|won.t power on"),
    ("software_app", r"crash|crashes|crashed|freeze|freezes|frozen|error|bug|glitch|not working|doesn.t work|won.t work|slow|stuck|missing|sound stops|app.*problem"),
]

def rule_intent(text: str) -> str:
    t = text or ""
    for intent, pattern in PATTERNS:
        if re.search(pattern, t, flags=re.I):
            return intent
    return "general_support"
