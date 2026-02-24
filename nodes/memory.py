from graph.state import GraphState
from langchain_core.messages import HumanMessage, AIMessage

# 每多少轮触发一次 summary 生成
SUMMARY_TRIGGER = 10  # 后续可以放入 config
KEEP_LAST_MESSAGES = 6   # summary 后保留最近多少条消息

def memory_node(state: GraphState):

    updates = {}

    #维护turncount
    turn_count = state.get("turn_count", 0) + 1
    updates["turn_count"] = turn_count
    
    messages=state.get("messages",[])
    summary=state.get("summary")

    # 决定是否生成 / 更新 summary 
    if turn_count % SUMMARY_TRIGGER == 0:
        return updates
        
    #构造用于summary的输入（覆盖式）
    dialogue_text=[]
    for m in messages:
        if isinstance(m,HumanMessage):
            dialogue_text.append(f"user:{m.content}")
        elif isinstance(m,AIMessage):
            dialogue_text.append(f"assistant:{m.content}")
            
    dialogue_text="\n".join(dialogue_text)
    
    #调用llm生成summary，假设已经有summarize_dialogue
    new_summary=summerize_dialogue(
        dialogue=dialogue_text,
        previous_summary=summary
    )
    #裁剪历史，summary之后只保留最近N条
    if len(messages)>KEEP_LAST_MESSAGES:
        updates["messages"]=messages[-KEEP_LAST_MESSAGES]

    return updates