from langgraph.graph import StateGraph, END
from .state import GraphState
from nodes.preprocess import preprocess_node
from nodes.emotion import emotion_node
from nodes.risk import risk_node
from nodes.safe_response import safe_response_node
from nodes.normal_response import normal_response_node
from nodes.self_critique import self_critique_node
from nodes.memory import memory_node
from nodes.persist import persist_node


def route_by_risk(state: GraphState) -> str:
    """
    0/1 -> normal_response
    或者1可以再细分?
    2 -> safe_response
    """
    level = state.get("risk_level", 0)
    return "safe_response" if level >= 1 else "normal_response"


def build_graph():
    g = StateGraph(GraphState)

    # 注册节点
    g.add_node("preprocess", preprocess_node)
    g.add_node("emotion", emotion_node)
    g.add_node("risk", risk_node)
    g.add_node("safe_response", safe_response_node)
    g.add_node("normal_response", normal_response_node)
    g.add_node("self_critique", self_critique_node)
    g.add_node("memory", memory_node)
    g.add_node("persist", persist_node)

    # 入口
    g.set_entry_point("preprocess")

    # 主干
    g.add_edge("preprocess", "emotion")
    g.add_edge("emotion", "risk")

    # 条件路由（risk -> safe/normal）
    g.add_conditional_edges(
        "risk",
        route_by_risk,
        {
            "safe_response": "safe_response",
            "normal_response": "normal_response",
        },
    )

    # 汇合到后处理链
    g.add_edge("safe_response", "self_critique")
    g.add_edge("normal_response", "self_critique")

    g.add_edge("self_critique", "memory")
    g.add_edge("memory", "persist")
    g.add_edge("persist", END)

    return g.compile()