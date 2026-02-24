import uuid
import time

from langchain_core.messages import HumanMessage
from graph.builder import build_graph

graph = build_graph()


def run_once(user_input: str):

    state = {
        "messages": [HumanMessage(content=user_input)],
        "user_id": "test_user",
        "session_id": str(uuid.uuid4()),
        "turn_count": 0,

        "response": None,

        "risk_level": 0,
        "risk_reason": None,

        "summary": None,

        "emotion": None,
    }

    result = graph.invoke(state)

    print("RESPONSE:", result.get("response"))


if __name__ == "__main__":
    run_once("hello")