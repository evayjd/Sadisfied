import uuid
from langchain_core.messages import HumanMessage
from graph.builder import build_graph

graph = build_graph()


def run_chat():
    import uuid
    from langchain_core.messages import HumanMessage

    session_id = str(uuid.uuid4())

    state = {
        "messages": [],
        "user_id": "test_user",
        "session_id": session_id,
        "turn_count": 0,
        "response": None,
        "risk_level": 0,
        "risk_reason": None,
        "summary": None,
        "emotion": None,
    }

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        state["messages"].append(HumanMessage(content=user_input))

        state = graph.invoke(state)

        print("Assistant:", state.get("response"))


if __name__ == "__main__":
    run_chat()