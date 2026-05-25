import sys
from langchain_deepseek import ChatDeepSeek
from tools.model_config import DeepSeek_model_config
from tools.helper import stream_print_with_reasoning
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

sys.stdout.reconfigure(encoding="utf-8")

# 模型的初始化
model = ChatDeepSeek(**DeepSeek_model_config)

# 1. 构造示例集 —— 给大模型参考的"答题样板"
examples = [
    {"word": "开心", "emoji": "😊"},
    {"word": "难过", "emoji": "😢"},
    {"word": "愤怒", "emoji": "😡"},
    {"word": "爱你", "emoji": "❤️"},
]

# 2. 定义单个示例的模板：如何格式化 examples 中的每条数据
example_prompt = PromptTemplate.from_template("词语：{word}\n对应的emoji：{emoji}")

# 3. 组装 FewShotPromptTemplate
chat_prompt_result = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="请根据下方示例的规律，为最后一个词语也配上对应的emoji：",
    suffix="词语：{word}\n对应的emoji：",
    input_variables=["word"],
)

# 4. 格式化后查看最终 prompt（调试用）
print("=" * 50)
print("最终发送给模型的 prompt：\n")
print(chat_prompt_result.invoke({"word": "震惊"}).text)
print("=" * 50)

# 5. 发送给模型，获取并流式输出回答
stream_print_with_reasoning(model.stream(chat_prompt_result.invoke({"word": "震惊"})))
