from langchain_core.messages import AIMessage
from graph.state import GraphState

CRISIS_TEMPLATE = (
        """I noticed that you might be experiencing some intense pain or distress right now. 
        If you are in immediate danger, 
        please reach out to local emergency services or someone you trust right away. 
        Whenever you're ready, could you tell me—what is the most difficult thing you're facing at this moment?"
    """
    )

def safe_response_node(state: GraphState):

    text = CRISIS_TEMPLATE

    return {
        "response": text,
        "messages": state["messages"] + [AIMessage(content=text)]
    }