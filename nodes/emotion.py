from graph.state import GraphState

def emotion_node(state: GraphState) -> dict:
    return{
        "emotion": {
            "label": "/",
                "confidence": 0.0,
                "reason": "/",
                "secondary": None,
                "distribution": None,
                "meta": {"model": "emotion_stub", "version": "v1"}
        }
    }