from unittest.mock import patch
from nodes.self_critique import self_critique_node

def test_self_critique_no_response():
    state = {"response": None}
    updates = self_critique_node(state)
    assert updates == {}