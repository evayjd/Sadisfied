from graph.state import GraphState


SUMMARY_TRIGGER = 10  # 之后可以放进 config


def memory_node(state: GraphState):

    turn_count = state.get("turn_count", 0)
    
    #todo：未来在这里做长对话压缩+构建context_messages，token预算控制？

    # 占位：如果达到阈值就生成 summary
    if turn_count > 0 and turn_count % SUMMARY_TRIGGER == 0:
        # 未来这里会调用 LLM 生成 summary
        return {
            "summary": "PLACEHOLDER_SUMMARY"
        }

    return {}