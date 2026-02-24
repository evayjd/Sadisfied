from typing import Dict, Any
import logging

from langchain_core.messages import HumanMessage
from graph.state import GraphState
from db.repo import Repository
from db.models import init_db
from config import DATABASE_URL

# 初始化 DB 与 Repo（简单版本，后续可优化为单例）
engine = init_db(DATABASE_URL)
repo = Repository(engine)

logger = logging.getLogger(__name__)


def persist_node(state: GraphState) -> Dict[str, Any]:
    
    user_id = state.get("user_id")
    session_id = state.get("session_id")

    if not user_id or not session_id:
        logger.error("Missing user_id or session_id in state")
        return {}

    try:
        # 保存 emotion（中间分析结果）
        if state.get("emotion"):
            repo.save_emotion(user_id, session_id, state["emotion"])

        # 保存 risk（即使是 0 也记录，方便审计）
        repo.save_risk(
            user_id=user_id,
            session_id=session_id,
            risk_level=state.get("risk_level", 0),
            risk_reason=state.get("risk_reason"),
        )

        # 保存本轮 user 消息
        user_text = None
        for m in reversed(state.get("messages", [])):
            if isinstance(m, HumanMessage):
                user_text = m.content
                break

        if user_text:
            repo.save_message(
                user_id=user_id,
                session_id=session_id,
                role="user",
                content=user_text,
            )

        # 保存 assistant 回复
        if state.get("response"):
            repo.save_message(
                user_id=user_id,
                session_id=session_id,
                role="assistant",
                content=state["response"],
            )

    except Exception as e:
        logger.exception(f"Persist node failed: {e}")

    return {}

   