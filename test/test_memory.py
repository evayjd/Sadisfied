from nodes.memory import memory_node


def test_turn_count_increment():
    state = {
        "turn_count": 0,
        "messages": [],
        "summary": None
    }

    updates = memory_node(state)

    assert updates["turn_count"] == 1
    assert "summary" not in updates