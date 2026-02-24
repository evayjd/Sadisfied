from typing import TypedDict, List, Optional, Annotated, Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    user_id : str
    session_id : Optional[str]
    turn_count : int
    
    response : Optional[str]
    
    risk_level : int # 0: low, 1: medium, 2: high
    risk_reason : Optional[str]
    
    summary : Optional[str]
    
    emotion: Optional[Dict[str, Any]]
    
    """"我目前期望emotion返回的格式
    emotion": {
    "label": "...",
    "confidence": 0.0,
    "reason": "...",
    "secondary": None,
    "distribution": None,情绪分布概率
    "meta": {...}可能没必要
}
"""