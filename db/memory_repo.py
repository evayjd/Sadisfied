from __future__ import annotations

import json
from typing import Any, Dict, Optional

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from db.redis_client import get_redis_client

def _state_key(session_id: str) -> str:
    return f"session:{session_id}:state"

#消息序列化，变成json可存格式
def _serialize_message(msg: BaseMessage) -> Dict[str, str]:
    if isinstance(msg, HumanMessage):
        role = "user"
    elif isinstance(msg, AIMessage):
        role = "assistant"
    else:
        role = msg.type  # fallback

    return {
        "role": role,
        "content": msg.content,
    }

#反序列化，给graph用❤️
def _deserialize_message(data: Dict[str, str]) -> BaseMessage:
    role = data.get("role")
    content = data.get("content", "")

    if role == "user":
        return HumanMessage(content=content)
    elif role == "assistant":
        return AIMessage(content=content)
    else:
        # fallback: treat as assistant
        return AIMessage(content=content)


#整个state的序列化和反序列化

def _serialize_state(state: Dict[str, Any]) -> Dict[str, Any]:
    state = dict(state)  

    messages = state.get("messages", [])
    state["messages"] = [_serialize_message(m) for m in messages]

    return state


def _deserialize_state(data: Dict[str, Any]) -> Dict[str, Any]:
    state = dict(data)

    messages = state.get("messages", [])
    state["messages"] = [_deserialize_message(m) for m in messages]

    return state


#从redis读某session状态
def load_state(session_id: str) -> Optional[Dict[str, Any]]:

    client = get_redis_client()
    raw = client.get(_state_key(session_id))

    if raw is None:
        return None

    data = json.loads(raw)
    return _deserialize_state(data)

#保存当前对话状态
def save_state(
    session_id: str,
    state: Dict[str, Any],
    ttl: Optional[int] = None,
) -> None:

    client = get_redis_client()

    data = _serialize_state(state)
    raw = json.dumps(data, ensure_ascii=False)

    key = _state_key(session_id)
#自动会话过期机制
    if ttl is not None:
        client.setex(key, ttl, raw)
    else:
        client.set(key, raw)

#用户可以手动清除对话
def delete_state(session_id: str) -> None:
    client = get_redis_client()
    client.delete(_state_key(session_id))