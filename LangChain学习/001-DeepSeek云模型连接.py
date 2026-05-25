from langchain_deepseek import ChatDeepSeek
from tools.model_config import DeepSeek_model_config
from tools.helper import stream_print_with_reasoning

model = ChatDeepSeek(**DeepSeek_model_config)

chunks = model.stream("你是谁？我是谁？")

stream_print_with_reasoning(chunks)
