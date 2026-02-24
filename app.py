import uuid
from dotenv import load_dotenv
load_dotenv()

import gradio as gr
from langchain_core.messages import HumanMessage
from graph.builder import build_graph

graph = build_graph()


def init_state():
    return {
        "messages": [],
        "user_id": "test_user",
        "session_id": str(uuid.uuid4()),
        "turn_count": 0,
        "response": None,
        "risk_level": 0,
        "risk_reason": None,
        "summary": None,
        "emotion": None,
    }


def chat(user_input, state):
    state["messages"].append(HumanMessage(content=user_input))
    state = graph.invoke(state)
    return state.get("response"), state


with gr.Blocks() as demo:

    state = gr.State(init_state())

    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Type your message...")

    def respond(message, chat_history, state):

        #  调用后端
        reply, state = chat(message, state)

        # 更新前端聊天记录
        chat_history.append({
            "role": "user",
            "content": message
        })

        chat_history.append({
            "role": "assistant",
            "content": reply
        })

        # 返回更新
        return "", chat_history, state

    msg.submit(
        respond,
        inputs=[msg, chatbot, state],
        outputs=[msg, chatbot, state]
    )

demo.launch()