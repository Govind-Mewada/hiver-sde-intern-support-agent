"""Brand-specific intent taxonomy derived from exploratory AppleSupport samples."""

INTENTS = {
    "device_update_problem": "iOS/macOS update causes a device or app problem",
    "battery_power": "battery life, charging, overheating or power issue",
    "account_access": "Apple ID, password, lockout or account access issue",
    "icloud": "iCloud storage, sync, backup or iCloud access issue",
    "app_store_itunes": "App Store, iTunes, app purchase/download issue",
    "billing_charge": "unexpected charge, payment, billing or purchase dispute",
    "apple_pay": "Apple Pay or wallet payment issue",
    "connectivity": "Wi-Fi, cellular, Bluetooth or connectivity problem",
    "device_hardware": "physical device/hardware issue or device not working",
    "order_delivery": "device order, reservation, delivery or shipment issue",
    "software_app": "software/app behavior not covered by update/connectivity",
    "general_support": "request for help, information, or an issue too ambiguous to classify",
}

# Conservative keyword rules are intentionally transparent and are used only for
# the offline baseline / bootstrapping. The production path can replace them with
# an LLM classifier without changing the evaluation interface.
RULES = [
    ("order_delivery", ["order", "delivery", "delivered", "shipping", "shipment", "reserved", "reservation"]),
    ("billing_charge", ["charged", "charge", "billing", "refund", "money back", "payment"]),
    ("apple_pay", ["apple pay", "wallet"]),
    ("icloud", ["icloud", "i cloud"]),
    ("account_access", ["apple id", "password", "locked out", "account locked", "verification code", "sign in"]),
    ("app_store_itunes", ["app store", "itunes", "download app", "in-app purchase"]),
    ("battery_power", ["battery", "charging", "charger", "overheating", "overheat"]),
    ("connectivity", ["wifi", "wi-fi", "bluetooth", "cellular", "network", "internet"]),
    ("device_update_problem", ["ios update", "ios 11", "ios 12", "ios 13", "ios 14", "ios 15", "ios 16", "ios 17", "ios 18", "update", "updated"]),
    ("device_hardware", ["screen", "display", "broken", "cracked", "camera", "speaker", "microphone"]),
    ("software_app", ["crash", "crashes", "freezes", "not working", "error", "bug"]),
]

def rule_intent(text: str) -> str:
    t = (text or "").lower()
    for intent, terms in RULES:
        if any(term in t for term in terms):
            return intent
    return "general_support"
