from unittest.mock import patch
from nodes.memory import memory_node
from langchain_core.messages import HumanMessage


def test_summary_trigger():
    state = {
        "turn_count": 11,  # 下一轮触发 12
        "messages": [HumanMessage(content="hello")] * 5,
        "summary": None
    }

    with patch("nodes.memory.summarize_dialogue", return_value="mock summary"):
        updates = memory_node(state)

    assert updates["turn_count"] == 12
    assert updates["summary"] == "mock summary"