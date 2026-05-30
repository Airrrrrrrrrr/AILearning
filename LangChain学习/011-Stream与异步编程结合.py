"""
=== 011 - Stream 与异步编程结合 ===

【学习目标】
1. 掌握 chain.astream() 异步流式输出
2. 理解 astream_events() 的事件生命周期
3. 将完整的 prompt | model | parser 链改写为异步版本
4. 实现异步并发场景：同时运行多条链

【核心知识点】
- chain.astream()：异步版本的流式迭代器，用 async for 遍历
- astream_events(version="v2")：获取链中每个 Runnable 的详细事件
  - on_chain_start / on_chain_end()：链的启停
  - on_llm_stream(on_chat_model_stream)：模型的流式 Token
  - on_parser_start / on_parser_end：解析器的输入输出
- 异步 RunnableLambda：传入 async def 函数
- 异步环境中的 RunnablePassthrough 用法不变

【练习步骤】
1. 将 005 的 prompt | model | StrOutputParser 链改写为异步：ainvoke() 和 astream()
2. 用 astream_events() 打印链执行的生命周期事件，标注每个环节的时间戳
3. 异步 RunnableLambda：用 async def 定义转换函数，放入链中
4. 并发场景：asyncio.gather() 同时运行 2 条不同的链，各自流式输出

【预期产出】
- 同步链 vs 异步链代码对比
- astream_events 事件流全览
- 并发双链的执行效果

【提示】
- astream_events 的 event 结构：{"event": "on_llm_stream", "data": {"chunk": ...}, ...}
- 异步 RunnableLambda 传入 async 函数即可，不需要额外包装
- 并发场景可以用 asyncio.create_task() 分别管理两条链的输出
- 注意：astream_events version="v2" 是推荐版本
"""

import sys
import os
import shutil
import asyncio
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from tools.model_config import DeepSeek_model_config
from tools.helper import astream_print_with_reasoning
from rich.live import Live
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

model = ChatDeepSeek(**DeepSeek_model_config)

prompt_geo = PromptTemplate.from_template(
    "{position}的经纬度是多少，将回答的结果封装成JSON的格式返回。"
    "要求key为lng和lat，value为对应经纬度的值。请严格遵循格式要求。"
)

chain = prompt_geo | model | StrOutputParser()
chain_raw = prompt_geo | model


# ========== 步骤1：同步链 vs 异步链对比 ==========

async def step1_sync_vs_async():
    print("=" * 50)
    print("步骤1：同步 invoke vs 异步 ainvoke 对比")
    print("=" * 50)

    start = time.time()
    sync_result = chain.invoke({"position": "东京"})
    sync_time = time.time() - start
    print(f"同步结果: {sync_result}")
    print(f"同步耗时: {sync_time:.2f}s\n")

    start = time.time()
    async_result = await chain.ainvoke({"position": "巴黎"})
    async_time = time.time() - start
    print(f"异步结果: {async_result}")
    print(f"异步耗时: {async_time:.2f}s\n")

    print("异步流式输出 astream（带reasoning）：")
    await astream_print_with_reasoning(chain_raw.astream({"position": "伦敦"}))


# ========== 步骤2：astream_events 事件生命周期 ==========

async def step2_astream_events():
    print("\n" + "=" * 50)
    print("步骤2：astream_events 事件生命周期")
    print("=" * 50)

    event_counts = {}
    async for event in chain.astream_events(
        {"position": "马尔代夫"}, version="v2"
    ):
        event_name = event["event"]
        event_counts[event_name] = event_counts.get(event_name, 0) + 1

        if event_name == "on_chain_start":
            print(f"\n[开始] 链启动: {event['name']}")
        elif event_name == "on_prompt_start":
            print(f"  [Prompt] 开始构建: {event['name']}")
        elif event_name == "on_chat_model_start":
            print(f"  [LLM] 开始调用模型: {event['name']}")
        elif event_name == "on_chat_model_stream":
            chunk = event["data"].get("chunk")
            if chunk:
                content = chunk.content if hasattr(chunk, "content") else str(chunk)
                if content:
                    sys.stdout.write(content)
                    sys.stdout.flush()
        elif event_name == "on_chat_model_end":
            print(f"\n  [LLM] 模型调用完成")
        elif event_name == "on_parser_start":
            print(f"  [Parser] 开始解析: {event['name']}")
        elif event_name == "on_parser_stream":
            output = event["data"].get("chunk")
            if output:
                sys.stdout.write(str(output))
                sys.stdout.flush()
        elif event_name == "on_parser_end":
            print(f"\n  [Parser] 解析完成")
        elif event_name == "on_chain_end":
            print(f"[结束] 链完成: {event['name']}")

    print(f"\n事件统计: {event_counts}")


# ========== 步骤3：异步 RunnableLambda ==========

async def step3_async_lambda():
    print("\n" + "=" * 50)
    print("步骤3：异步 RunnableLambda")
    print("=" * 50)

    async def add_prefix(text: str) -> str:
        await asyncio.sleep(0.01)
        return f"[异步处理] {text}"

    async def count_words(text: str) -> str:
        await asyncio.sleep(0.01)
        return f"{text} (字数: {len(text)})"

    chain_with_lambda = (
        prompt_geo
        | model
        | StrOutputParser()
        | RunnableLambda(add_prefix)
        | RunnableLambda(count_words)
    )

    result = await chain_with_lambda.ainvoke({"position": "上海"})
    print(f"带异步Lambda的结果:\n{result}")


# ========== 步骤4：并发双链流式输出 ==========

async def step4_concurrent_streams():
    print("\n" + "=" * 50)
    print("步骤4：并发双链流式输出（终端分屏）")
    print("=" * 50)

    prompt_weather = PromptTemplate.from_template("{city}今天天气怎么样？用一句话回答。")
    chain_weather = prompt_weather | model

    prompt_food = PromptTemplate.from_template("{city}有什么特色美食？用一句话回答。")
    chain_food = prompt_food | model

    left_text = Text(no_wrap=False, overflow="fold")
    right_text = Text(no_wrap=False, overflow="fold")
    left_done = asyncio.Event()
    right_done = asyncio.Event()

    terminal_width = shutil.get_terminal_size().columns
    panel_width = max(15, (terminal_width - 1) // 2)
    left_panel = Panel(left_text, title="天气链", border_style="cyan", width=panel_width)
    right_panel = Panel(right_text, title="美食链", border_style="green", width=panel_width)


    async def stream_to_text(text_obj, done_event, astream):
        had_reasoning = False
        async for chunk in astream:
            reasoning = chunk.additional_kwargs.get("reasoning_content", "") if isinstance(chunk.additional_kwargs, dict) else ""
            content = chunk.content or ""
            if reasoning:
                if not had_reasoning:
                    text_obj.append("推理过程：\n", style="dim")
                    had_reasoning = True
                text_obj.append(reasoning, style="dim")
            if content:
                if had_reasoning:
                    text_obj.append("\n── 回答 ──\n", style="dim")
                    had_reasoning = False
                text_obj.append(content)
        done_event.set()

    start = time.time()
    with Live(Columns([left_panel, right_panel], expand=False), refresh_per_second=10, screen=True):
        await asyncio.gather(
            stream_to_text(left_text, left_done, chain_weather.astream({"city": "北京"})),
            stream_to_text(right_text, right_done, chain_food.astream({"city": "成都"})),
        )
    total_time = time.time() - start

    rprint(Columns([left_panel, right_panel], expand=False))
    print(f"\n并发总耗时: {total_time:.2f}s（两条链同时执行）")
    input("\n按回车键退出...")


# ========== 主入口 ==========

async def main():
    # await step1_sync_vs_async()
    # await step2_astream_events()
    # await step3_async_lambda()
    await step4_concurrent_streams()


asyncio.run(main())
