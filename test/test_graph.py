from unittest.mock import patch
from langchain_core.messages import HumanMessage
from graph.builder import build_graph


def test_graph_risk_flow():
    graph = build_graph()

    state = {
        "messages": [HumanMessage(content="I am hopeless")],
        "user_id": "test_user",
        "session_id": "test_session",
        "turn_count": 0,
        "summary": None,
        "response": None,
        "risk_level": 0,
        "risk_reason": None,
        "emotion": None,
    }

    with patch("services.llm.LLMService.generate", return_value="Mock reply"):
        new_state = graph.invoke(state)

    assert "risk_level" in new_state
    assert "response" in new_state
    assert new_state["response"] == "Mock reply"