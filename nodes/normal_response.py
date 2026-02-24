from langchain_core.messages import AIMessage
from graph.state import GraphState
from services.llm import LLMService

def normal_response_node(state: GraphState):

    messages = state["messages"]

    text = LLMService.generate(messages)

    return {
        "response": text,
        "messages": [AIMessage(content=text)]
    }