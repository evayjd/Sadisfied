import pytest
from services.safety_rules import SafetyRules


@pytest.mark.parametrize(
    "distribution,expected_level",
    [
        ({"despair": 0.7}, 2),
        ({"despair": 0.4}, 1),
        ({"despair": 0.1}, 0),
    ]
)
def test_risk_levels(distribution, expected_level):
    emotion = {
        "label": "despair",
        "confidence": 0.5,
        "distribution": distribution
    }

    level, _ = SafetyRules.assess(emotion)

    assert level == expected_level