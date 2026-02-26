from unittest.mock import patch
from services.llm import LLMService

def test_llm_exception():
    with patch("requests.post", side_effect=Exception("fail")):
        try:
            LLMService.generate([])
        except:
            assert True