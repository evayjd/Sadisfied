from langchain_core.messages import HumanMessage
from services.llm import LLMService


SUMMARY_SYSTEM_PROMPT = """
You are a dialogue summarization assistant.
Compress conversation history while preserving:
- key facts
- emotional signals
- safety risks
Be concise and factual.
"""

def summarize_dialogue(dialogue: str, previous_summary: str | None):
    #旧摘要+新对话判断同时合并
    if previous_summary:
        content = (
            "We have an existing conversation summary.\n\n"
            f"Previous summary:\n{previous_summary}\n\n"
            f"New dialogue:\n{dialogue}\n\n"
            "Update the summary concisely, preserving key facts, emotions and risks."
        )
    #首次生成
    else:
        content = (
            f"Dialogue:\n{dialogue}\n\n"
            "Provide a concise summary preserving key facts, emotions and risks."
        )

    messages = [
        HumanMessage(content=content)
    ]

    

    return LLMService.generate(
        messages,
        system_prompt=SUMMARY_SYSTEM_PROMPT
    ).strip()