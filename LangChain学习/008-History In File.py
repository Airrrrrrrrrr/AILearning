"""
@Author  : Jsy
@Date    : 2026/5/2715:21
@Description : 将会话保存在文件中，实现长期记忆
"""
import os
import json
from typing import Sequence

from langchain_core.runnables.history import RunnableWithMessageHistory
from tools.model_config import DeepSeek_model_config
from langchain_deepseek import ChatDeepSeek
from tools.helper import stream_print_with_reasoning
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import messages_from_dict, message_to_dict, BaseMessage

model = ChatDeepSeek(**DeepSeek_model_config)


class FileChatMessageHistory(BaseChatMessageHistory):

    def __init__(self, storage_path: str, session_id: str):
        self.storage_path = storage_path
        self.session_id = session_id

    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(
                os.path.join(self.storage_path, self.session_id),
                "r",
                encoding="utf-8",
            ) as f:
                messages_data = json.load(f)
            return messages_from_dict(messages_data)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)

        serialized = [message_to_dict(message) for message in all_messages]
        file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(serialized, f)

    def clear(self) -> None:
        file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


store = {}
storage_dir = os.path.join(os.path.dirname(__file__), "chat_histories")
session_id = "Jsy"


def get_session_history(sid: str):
    if sid not in store:
        store[sid] = FileChatMessageHistory(
            storage_path=storage_dir,
            session_id=f"{sid}.json",
        )
    return store[sid]


prompt = ChatPromptTemplate.from_template("<{history}>根据如上历史消息回复我。\n我的输入：{input}")

chain_with_history = RunnableWithMessageHistory(
    prompt | model,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

print(f"=== 交互式多轮对话（历史持久化到 {storage_dir}） ===")
print("输入 'Exit' 或 '退出' 结束对话，输入 'clear' 清除当前会话历史\n")

while True:
    user_input = input("你：").strip()
    if user_input.lower() == "exit" or user_input == "退出":
        print("对话结束。历史已保存到文件，下次运行可继续。")
        break
    if user_input.lower() == "clear":
        get_session_history(session_id).clear()
        print("当前会话历史已清除。")
        continue
    if not user_input:
        continue

    stream_print_with_reasoning(
        chain_with_history.stream(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}},
        )
    )
