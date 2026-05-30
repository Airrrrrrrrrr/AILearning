"""
=== 009 - 异步编程基础 (async/await) ===

【学习目标】
1. 理解 async/await 基本语法和事件循环
2. 掌握 asyncio.gather() 并发执行多个异步任务
3. 对比同步 invoke() vs 异步 ainvoke() 的性能差异
4. 用 astream() 实现异步流式输出

【核心知识点】
- async def 定义协程函数，await 等待异步操作完成
- asyncio.run() 启动事件循环，执行协程
- async for 遍历异步生成器（如 astream 返回的异步迭代器）
- asyncio.gather(*tasks) 并发运行多个协程，返回结果列表

【练习步骤】
1. 用 await model.ainvoke() 发送单个异步请求，对比 invoke() 耗时
2. 用 asyncio.gather() 同时发送 3 个独立问题，计时验证并发加速
3. 用 async for chunk in model.astream(...) 实现异步流式打印
4. 将 helper.py 中的 stream_print_with_reasoning 改写为异步版本

【预期产出】
- 同步 vs 异步耗时对比数据
- 异步流式输出效果展示

【提示】
- ChatDeepSeek 的 ainvoke() 和 astream() 是原生支持的
- gather 中的每个任务必须是协程调用（加 await 会变成同步）
- 可以用 asyncio.create_task() 或直接 gather 传入协程
"""
import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from langchain_deepseek import ChatDeepSeek
from tools.model_config import DeepSeek_model_config
from tools.helper import *
from langchain_core.prompts import PromptTemplate
from tools.time_tools import spent_time, spent_time_async

@spent_time_async
async def response_ainvoke(myChain, input_text):
    response = await myChain.ainvoke({"text":input_text})
    return response


@spent_time
def response_invoke(myChain, input_text):
    response = myChain.invoke({"text":input_text})
    return response

@spent_time_async
async def response_ainvoke_muti(myChain, input_text_list):
    results = await asyncio.gather(response_ainvoke(myChain, input_text_list[0]),
                                   response_ainvoke(myChain, input_text_list[1]),
                                   response_ainvoke(myChain, input_text_list[2]),
                                   return_exceptions=True)
    return results



model = ChatDeepSeek(**DeepSeek_model_config)

prompt = PromptTemplate.from_template("{text}")

chain = prompt | model

text = "1. 理解 async/await 基本语法和事件循环\n2. 掌握 asyncio.gather() 并发执行多个异步任务"

# responseA = asyncio.run(response_ainvoke(chain, text))
# invoke_print(responseA)

# responseB = response_invoke(chain, text)
# invoke_print(responseB)

# text_list = ['大海是什么味道的？','天有多高？','地有多厚？']
# responseC = asyncio.run(response_ainvoke_muti(chain, text_list))
# for response in responseC:
#     invoke_print(response)

async def concurrent_stream_demo(myChain, questions):
    """
    并发流式：同时向模型发送多个请求，各自流式输出
    每个请求前加上标签，方便区分不同流的输出
    """
    async def stream_with_label(label, question):
        print(f"\n{'='*20} {label} 开始 {'='*20}")
        full = await astream_print_with_reasoning(myChain.astream({"text": question}))
        print(f"{'='*20} {label} 结束 {'='*20}\n")
        return full

    results = await asyncio.gather(
        stream_with_label("问题A", questions[0]),
        stream_with_label("问题B", questions[1]),
    )
    return results


questions = ["什么是Python？", "什么是JavaScript？"]
asyncio.run(concurrent_stream_demo(chain, questions))
