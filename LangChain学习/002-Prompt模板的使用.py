from langchain_deepseek import ChatDeepSeek
from tools.model_config import DeepSeek_model_config
from tools.helper import stream_print
from langchain_core.prompts import PromptTemplate

# 模型的初始化
model = ChatDeepSeek(**DeepSeek_model_config)

prompt_template = PromptTemplate.from_template("你觉得{things}怎么样？")
# prompt_template 是一个  “Runnable” , 所以可以执行invoke
prompt_template_text = prompt_template.invoke({"things":"安卓系统"})

# 此时仅仅只是将prompt填充完整了，还未向model传输prompt
print("填充后的prompt：", prompt_template_text)

# 将prompt向model传输，得到chunks（模型流式输出下返回的可迭代对象）
chunks = model.stream(prompt_template_text)

# 带思考过程的打印
stream_print_with_reasoning(chunks)
