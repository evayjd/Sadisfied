from langchain_core.messages import HumanMessage
from services.emotion_classifier import EmotionClassifier

def test_despair_detection():
    messages = [HumanMessage(content="I want to kill myself")]
    result = EmotionClassifier.classify(messages)
    assert result["label"] == "despair"