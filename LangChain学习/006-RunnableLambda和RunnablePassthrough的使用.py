import json
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_deepseek import ChatDeepSeek
from tools.model_config import DeepSeek_model_config
from langchain_core.prompts import PromptTemplate


myfuncA = RunnableLambda(
    lambda data: {**json.loads(data.content), "key":"value"}
)
# myfuncA中接收的data是AIMessage对象，为model的输出，仅此而已，这里的key和value是写死的值。
model = ChatDeepSeek(**DeepSeek_model_config)

prompt_templateA = PromptTemplate.from_template("{position}的经纬度是多少，将回答的结果封装成JSON的格式返回。要求key为lng和lat，value为对应经纬度的值。请严格遵循格式要求。")

chainA = prompt_templateA | model | myfuncA

print(chainA.invoke({"position": "北京"}))

myfuncB = RunnableLambda(
    lambda data: {**json.loads(data["response"].content), "position":data["position"]}
)
# myfuncB 接收的 data 是 AIMessage 和初始输入的 position 组成的 dict 。
# 因为执行 RunnablePassthrough.assign(response=prompt_templateA | model) ，这是一个透传赋值操作，
# 将model返回的 AIMessage 以 response 为 key 附加到 dict{"position": "北京"} 中 ---> {"position": "北京", "response": AIMessage(content='',...)}。

chainB = RunnablePassthrough.assign(response=prompt_templateA | model) | myfuncB

print(chainB.invoke({"position": "北京"}))
