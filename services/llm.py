from typing import List
from langchain_core.messages import BaseMessage

class LLMService:

    @staticmethod
    def generate(messages: List[BaseMessage]) -> str:
        """
        llm接口
        输入：完整消息列表
        输出：字符串回复
        """

        # 占位符版本（后面接 OpenAI或其他便宜的）
        return "PLACEHOLDER_RESPONSE"