import json
from graph.state import GraphState
from services.llm import LLMService


CRITIQUE_SYSTEM_PROMPT = """
你是一名对话质量与安全审查专家。

请对 assistant 回复进行审查，并返回 JSON 格式：

{
  "approved": true/false,
  "reason": "简要说明",
  "improved_response": "如果需要修改，给出完整改写；否则为 null"
}

审查标准：
1. 是否存在潜在风险
2. 是否逻辑不清晰
2. 是否语气不合适
4. 是否偏离用户问题

只返回 JSON，不要输出其他文本。
"""


def self_critique_node(state: GraphState):

    original_response = state.get("response")

    if not original_response:
        return {}

    critique_input = [
        {"role": "system", "content": CRITIQUE_SYSTEM_PROMPT},
        {"role": "user", "content": original_response},
    ]

    try:
        raw_output = LLMService.generate(critique_input)
        result = json.loads(raw_output)
    except Exception:
        # 解析失败直接放行
        return {}

    # 如果批准
    if result.get("approved", True):
        return {}

    improved = result.get("improved_response")

    # 防止模型胡乱输出
    if not improved:
        return {}

    # 防止过度扩写
    if len(improved) > 2 * len(original_response):
        return {}

    return {
        "response": improved.strip()
    }