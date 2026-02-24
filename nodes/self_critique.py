from graph.state import GraphState
from services.llm import LLMService


def self_critique_node(state: GraphState):

    original_response = state.get("response", "")

    # 未来这里会构造 critique prompt
    # critique = LLMService.generate([...])

    # 现在先占位，不修改 response
    return {}