from typing import List

from langchain_core.prompt_values import ChatPromptValue
from langchain_deepseek import ChatDeepSeek
from tools.model_config import DeepSeek_model_config
from tools.helper import stream_print_with_reasoning
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, AIMessagePromptTemplate

# 模型的初始化
model = ChatDeepSeek(**DeepSeek_model_config)

# 创建一个聊天对话的prompt模板，from_messages（多轮对话信息记录）

# 在chatPromptA中，每一个元组都是一个PromptTemplate对象，chatPromptA则是一个ChatPromptTemplate对象
chatPromptA:ChatPromptTemplate = ChatPromptTemplate.from_messages(
    [
        ("system","你是Skipper，马达加斯加的那只🐧老大！我是刚入队的🐧新兵，带领我完成上头考核的任务。"), # SystemMessagePromptTemplate
        ("human","老大，我们这是在哪？"), # HumanMessagePromptTemplate
        ("assistant","手势（嘘！你没看到前面的那头壮实狮子吗？！等他先过去，我们待会进入管道后，分头行动，拿回属于我们的罐头！）"), # AIMessagePromptTemplate
        ("human","手势（{words}）"), # HumanMessagePromptTemplate
    ]
)

# 元组形式：("角色", "文本") — 文本会被解析为模板
# ("human","手势（{words}）") 是一个 HumanMessagePromptTemplate，可以被invoke
text1:SystemMessage = SystemMessage(content="你是Skipper，马达加斯加的那只🐧老大！我是刚入队的🐧新兵，带领我完成上头考核的任务。")
text3:AIMessagePromptTemplate =("assistant","手势（嘘！你没看到前面的那头壮实狮子吗？！等他先过去，我们待会进入管道后，分头行动，拿回属于我们的罐头！）")

chatPromptB = ChatPromptTemplate.from_messages(
    [
        text1, # 这里是Message对象
        HumanMessage(content="老大，我们这是在哪？"),  # 这里是Message对象
        text3,
        ("human","{words}"), # HumanMessagePromptTemplate
    ]
)
# HumanMessage(content="手势（{words}）") 这里不可以被invoke，已经是一个Message了


chatPromptC = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history_talk")
    ]
)
history_talk = [
        ("system","你是Skipper，马达加斯加的那只🐧老大！我是刚入队的🐧新兵，带领我完成上头考核的任务。"), # SystemMessagePromptTemplate
        ("human","老大，我们这是在哪？"), # HumanMessagePromptTemplate
        ("assistant","手势（嘘！你没看到前面的那头壮实狮子吗？！等他先过去，我们待会进入管道后，分头行动，拿回属于我们的罐头！）"), # AIMessagePromptTemplate
        ("human","好的老（声音很大）大！（声音很小）"), # HumanMessagePromptTemplate
]


chatPromptA_result:List = chatPromptA.format_messages(words="捂嘴！好的老大！") # format_messages后得到的是List[Message]
chatPromptB_result:ChatPromptValue = chatPromptB.invoke({"words": "好的老（声音很大）大！（声音很小）"}) # invoke后得到的是ChatPromptValue
chatPromptC_result:ChatPromptValue = chatPromptC.invoke({"history_talk": history_talk})


# chatPromptA_Messages 不相等 chatPrompt_result
if chatPromptA != chatPromptB:
    print("chatPromptA 不相等 chatPromptB")
    print("ChatPromptValue AND List[Message] 都可以直接喂给model得到回复")
    print("\n" * 3)



stream_print_with_reasoning(model.stream(chatPromptA_result))
print("=" * 60)
print("\n" * 3)
stream_print_with_reasoning(model.stream(chatPromptB_result))
print("=" * 60)
print("\n" * 3)
stream_print_with_reasoning(model.stream(chatPromptC_result))

