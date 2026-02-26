from langchain_core.messages import HumanMessage, AIMessage
from nodes.safe_response import safe_response_node, CRISIS_TEMPLATE


def test_safe_response_returns_crisis_template():
    state = {
        "messages": [HumanMessage(content="I want to die")]
    }

    updates = safe_response_node(state)

    # response等于 crisis tem
    assert updates["response"] == CRISIS_TEMPLATE

    # messages 增加一条 AIMessage
    assert len(updates["messages"]) == 2
    assert isinstance(updates["messages"][-1], AIMessage)

    # AIMessage 内容等于 crisis 模板
    assert updates["messages"][-1].content == CRISIS_TEMPLATE


def test_safe_response_does_not_modify_original_messages():
    original_messages = [HumanMessage(content="Help me")]
    state = {"messages": original_messages.copy()}

    updates = safe_response_node(state)

    # 原列表长度应保持不变
    assert len(original_messages) == 1

    # 新列表应为旧列表 + 1
    assert len(updates["messages"]) == 2


def test_safe_response_structure():
    state = {
        "messages": [HumanMessage(content="I am hopeless")]
    }

    updates = safe_response_node(state)

    # 必须包含 response 和 messages
    assert "response" in updates
    assert "messages" in updates

    # response 类型应为字符串
    assert isinstance(updates["response"], str)

    # messages 应为列表
    assert isinstance(updates["messages"], list)