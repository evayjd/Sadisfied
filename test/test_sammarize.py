from services.summarize import summarize_dialogue
from unittest.mock import patch

def test_summarize_mock():
    with patch("services.summarize.LLMService.generate", return_value="summary"):
        result = summarize_dialogue("hello", None)
        assert result == "summary"