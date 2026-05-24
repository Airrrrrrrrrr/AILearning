import sys

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_deepseek import ChatDeepSeek
from tools.model_config import DeepSeek_model_config
from tools.helper import stream_print, stream_print_with_reasoning
from langchain_core.prompts import PromptTemplate

# 模型的初始化
model = ChatDeepSeek(**DeepSeek_model_config)

prompt_templateA = PromptTemplate.from_template("{position}的经纬度是多少，将回答的结果封装成JSON的格式返回。要求key为lng和lat，value为对应经纬度的值。请严格遵循格式要求。")

chainA = prompt_templateA | model # 通过__or__魔法方法来实现Runnable对象的链接

stream_print_with_reasoning(chainA.stream({"position":"马尔代夫"}))


prompt_templateB = PromptTemplate.from_template("我的经度为{lng}纬度为{lat}，给出我的具体地址")

chainB =  prompt_templateA | model | JsonOutputParser() | prompt_templateB |model

stream_print_with_reasoning(chainB.stream({"position":"北京"}))
