from services.safety_rules import SafetyRules

def test_high_risk():
    emotion = {
        "label": "despair",
        "confidence": 0.4,
        "distribution": {"despair": 0.7}
    }
    level, _ = SafetyRules.assess(emotion)
    assert level == 2