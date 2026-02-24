import uuid
from dotenv import load_dotenv
load_dotenv()

import gradio as gr
from langchain_core.messages import HumanMessage

from graph.builder import build_graph
from db.memory_repo import load_state

graph = build_graph()


def init_state(session_id: str):
    """
    Redis没有会话的时候,创建一个初始状态
    """
    return {
        "messages": [],
        "user_id": session_id,
        "session_id": session_id,
        "turn_count": 0,
        "response": None,
        "risk_level": 0,
        "risk_reason": None,
        "summary": None,
        "emotion": None,
    }


def chat(user_input: str, session_id: str):
    
    state = load_state(session_id)

    if state is None:
        state = init_state(session_id)

    state["messages"].append(HumanMessage(content=user_input))


    state = graph.invoke(state)

    return state.get("response"), state


#————构建UI————！！！！

with gr.Blocks() as demo:

    # 只存sessionid
    session_id_state = gr.State(str(uuid.uuid4()))

    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Type your message...")

    def respond(message, chat_history, session_id):
        # 调用后端
        reply, state = chat(message, session_id)

        chat_history = chat_history or []

        chat_history.append({
            "role": "user",
            "content": message
        })
        chat_history.append({
            "role": "assistant",
            "content": reply
        })

        return "", chat_history, session_id

    msg.submit(
        respond,
        inputs=[msg, chatbot, session_id_state],
        outputs=[msg, chatbot, session_id_state]
    )

demo.launch()