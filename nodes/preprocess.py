from langchain_core.messages import HumanMessage
from graph.state import GraphState

def preprocess_node(state: GraphState) -> dict:
    # 这里可以做一些输入清洗、格式化等预处理工作
    # 目前先直接返回原状态
    return state