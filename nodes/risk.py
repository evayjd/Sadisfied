from typing import Dict, Any
from graph.state import GraphState
from services.safety_rules import SafetyRules


def risk_node(state: GraphState) -> Dict[str, Any]:

    emotion = state.get("emotion")

    # 如果 emotion 不存在，默认低风险
    if not isinstance(emotion, dict):
        return {
            "risk_level": 0,
            "risk_reason": "No emotion data available"
        }

    try:
        level, reason = SafetyRules.assess(emotion)
        
    except Exception as e:
        # 降级处理：不要让 graph 崩溃
        return {
            "risk_level": 0,
            "risk_reason": f"Risk assessment failed: {str(e)}"
        }

    return {
        "risk_level": level,
        "risk_reason": reason
    }