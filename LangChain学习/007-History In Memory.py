"""
@Author  : Jsy
@Date    : 2026年5月27日15点02分
@Description : 在内存中的一次性多轮对话
"""
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_deepseek import ChatDeepSeek
from tools.model_config import DeepSeek_model_config
from tools.helper import stream_print_with_reasoning
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory

model = ChatDeepSeek(**DeepSeek_model_config)

prompt_no_history = ChatPromptTemplate.from_template("{input}")
prompt_with_history = ChatPromptTemplate.from_template("<{history}>根据如上历史消息回复我。\n我的输入：{input}")

chain_no_history = prompt_no_history | model
store = {}
session_id = "a"




def get_session_history(sid: str):
    if sid not in store:
        store[sid] = InMemoryChatMessageHistory()
    return store[sid]


chain_with_history = RunnableWithMessageHistory(
    prompt_with_history | model,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

print("=== 交互式多轮对话（输入 'Exit' 或 '退出' 结束） ===")
is_first_round = True

while True:
    user_input = input("\n你：").strip()
    if user_input.lower() == "exit" or user_input == "退出":
        print("对话结束。")
        break
    if not user_input:
        continue

    if is_first_round:
        response = stream_print_with_reasoning(chain_no_history.stream({"input": user_input}))
        get_session_history(session_id).add_user_message(user_input)
        get_session_history(session_id).add_ai_message(response)
        is_first_round = False
    else:
        stream_print_with_reasoning(
            chain_with_history.stream(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}},
            )
        )
