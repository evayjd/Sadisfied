import uuid
from dotenv import load_dotenv
load_dotenv()

import gradio as gr
# 补充导入AIMessage
from langchain_core.messages import HumanMessage, AIMessage

from graph.builder import build_graph
from db.memory_repo import load_state,save_state

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


MAX_HISTORY = 20  # 最多20条消息（用户+助手合计）

def chat(user_input: str, session_id: str):
    state = load_state(session_id)
    if state is None:
        state = init_state(session_id)

    state["messages"].append(HumanMessage(content=user_input))

    state = graph.invoke(state)
    
    save_state(session_id, state)

    return state.get("response"), state


#————构建UI————
with gr.Blocks() as demo:
    session_id_state = gr.State(None)
    gr.Markdown("""
>  **Privacy Warning**: To ensure your conversations remain private and aren't shared with others, 
> please use a **complex ID** combined with a **PIN**. 
> Think of it as your personal vault key! 🌟
""")
    with gr.Row():
        sid_input = gr.Textbox(
            label="user_session_id",
            placeholder="Enter your unique(🌟🌟🌟) ID",
            scale=4
        )
        
        set_btn=gr.Button("Confirm",variant="primary",scale=1)
    
    
    chatbot=gr.Chatbot(label="Chat History")
    msg = gr.Textbox(placeholder="Please enter your ID above to start chatting...",interactive=False)
    
    # 逻辑处理
    def handle_login(sid):
        if not sid or sid.strip()=="":
            return gr.update(interactive=False),None,"Please enter a valid ID"
        state = load_state(sid)
        history=[]
        if state and "messages" in state:
            messages = state["messages"]
            
            i = 0
            while i < len(messages):
                # 只处理用户消息开头的成对消息
                if isinstance(messages[i], HumanMessage):
                    user_msg = messages[i].content
                    # 下一条是助手消息则取，否则为空
                    assistant_msg = messages[i+1].content if (i+1 < len(messages) and isinstance(messages[i+1], AIMessage)) else ""
                    history.append({"role": "user", "content": user_msg})
                    history.append({"role": "assistant", "content": assistant_msg})
                    i += 2
                else:
                    i += 1
        return gr.update(interactive=True,placeholder="You can start chatting now..."),sid,history


    def respond(message, chat_history, session_id):
        if not session_id:
            return "",chat_history+[{"role": "assistant", "content": "Please enter and confirm your ID first."}], session_id
        
        # 调用后端
        try:
            reply, state = chat(message, session_id)
        except Exception as e:
            reply = f"System error: {str(e)}"  

        chat_history = chat_history or []
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": reply})

        
        if len(chat_history) > MAX_HISTORY:
            chat_history = chat_history[-MAX_HISTORY:]

        return "", chat_history, session_id
    
    set_btn.click(
        handle_login,
        inputs=[sid_input],
        outputs=[msg,session_id_state,chatbot]
    )

    msg.submit(
        respond,
        inputs=[msg, chatbot, session_id_state],
        outputs=[msg, chatbot, session_id_state]
    )

demo.launch()