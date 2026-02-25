from langchain_core.messages import HumanMessage, SystemMessage
from graph.state import GraphState

# 冷启动 / 长对话时，最多保留多少条最近消息
MAX_RECENT_MESSAGES = 6  # 后续可放入 config，或修改


def preprocess_node(state: GraphState) -> dict:

    messages = state.get("messages", [])
    summary = state.get("summary")

    # 取最近的 messages，用于本轮推理窗口
    recent_messages = messages[-MAX_RECENT_MESSAGES:]

    # 如果存在 summary，拼接到上下文最前面 
    if summary:
        context_messages = [
            SystemMessage(
                content=f"以下是之前对话的总结：\n{summary}"
                )
        ] + recent_messages
    else:
        inference_messages = recent_messages

    return {
        "inference_messages": inference_messages
    }