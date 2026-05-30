"""
=== 010 - StructuredOutput 与 Pydantic 解析 ===

【学习目标】
1. 掌握 Pydantic BaseModel 定义数据结构
2. 使用 PydanticOutputParser 自动生成格式指令并解析输出
3. 使用 model.with_structured_output() 实现结构化输出（推荐方式）
4. 对比手动Prompt → JsonOutputParser → PydanticOutputParser 三种方式

【核心知识点】
- Pydantic BaseModel + Field：定义字段名、类型、描述、默认值
- PydanticOutputParser：get_format_instructions() 生成JSON Schema提示词
- with_structured_output(schema)：让模型直接返回符合schema的对象
- 嵌套模型：List[SubModel]、Optional字段、Union类型

【练习步骤】
1. 定义 MovieReview(BaseModel)，包含 title/str, rating/float, summary/str, pros/List[str], cons/List[str]
2. 方式A：用 PydanticOutputParser + prompt | model | parser 链
3. 方式B：用 model.with_structured_output(MovieReview) 直接调用
4. 尝试嵌套结构，如定义 Actor(BaseModel)，MovieReview 中包含 actors: List[Actor]
5. 测试 Optional 字段和默认值，观察模型不返回时的行为

【预期产出】
- 三种结构化输出方式的代码对比
- 复杂嵌套结构的解析结果

【提示】
- with_structured_output() 内部会调用模型的 tool_call 或 JSON mode
- DeepSeek 支持 function calling，可以直接用 with_structured_output
- Pydantic v2 用 model_json_schema() 查看生成的 JSON Schema
- 字段的 Field(description=...) 会帮助模型理解每个字段的含义
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from tools.model_config import DeepSeek_model_config

config_no_reasoning = {**DeepSeek_model_config,"extra_body":{"thinking": {"type": "disabled"}}}
del config_no_reasoning['reasoning_effort']
del config_no_reasoning['streaming']
model = ChatDeepSeek(**config_no_reasoning)


# ========== 步骤1：定义 Pydantic 数据模型 ==========

class Actor(BaseModel):
    """演员信息——嵌套子模型"""
    name: str = Field(description="演员姓名")
    role: str = Field(description="饰演的角色名")


class MovieReview(BaseModel):
    """电影评价结构化模型"""
    title: str = Field(description="电影名称")
    rating: float = Field(ge=0, le=10, description="评分，0到10之间")
    summary: str = Field(description="一句话总结这部电影")
    pros: List[str] = Field(description="电影的优点列表")
    cons: List[str] = Field(description="电影的缺点列表")
    actors: List[Actor] = Field(description="主要演员列表")
    sequel_hint: Optional[str] = Field(default=None, description="是否有续集计划，没有则为null")


# 查看自动生成的 JSON Schema
print("=" * 50)
print("MovieReview 生成的 JSON Schema：")
print(MovieReview.model_json_schema())
print("=" * 50)


# ========== 步骤2：方式A — PydanticOutputParser + LCEL 链 ==========

parser = PydanticOutputParser(pydantic_object=MovieReview)

prompt_A = PromptTemplate.from_template(
    "请对电影《{movie}》进行评价。\n\n"
    "{format_instructions}\n"
    "请严格按照上述JSON格式返回结果。"
).partial(format_instructions=parser.get_format_instructions())

chain_A = prompt_A | model | parser

result_A = chain_A.invoke({"movie": "盗梦空间"})
print("\n===== 方式A: PydanticOutputParser =====")
print(f"类型: {type(result_A)}")
print(f"电影: {result_A.title}")
print(f"评分: {result_A.rating}")
print(f"总结: {result_A.summary}")
print(f"优点: {result_A.pros}")
print(f"缺点: {result_A.cons}")
print(f"演员: {[(a.name, a.role) for a in result_A.actors]}")
print(f"续集: {result_A.sequel_hint}")


# ========== 步骤3：方式B — with_structured_output()（推荐） ==========

structured_model = model.with_structured_output(MovieReview, method="function_calling", strict=False)

result_B = structured_model.invoke("请对电影《星际穿越》进行评价")
print("\n===== 方式B: with_structured_output =====")
print(f"类型: {type(result_B)}")
print(f"电影: {result_B.title}")
print(f"评分: {result_B.rating}")
print(f"总结: {result_B.summary}")
print(f"优点: {result_B.pros}")
print(f"缺点: {result_B.cons}")
print(f"演员: {[(a.name, a.role) for a in result_B.actors]}")
print(f"续集: {result_B.sequel_hint}")


# ========== 步骤4：方式对比总结 ==========

print("\n===== 三种结构化输出方式对比 =====")
print("1. 手动Prompt + JsonOutputParser（005已学）：需自己写格式指令，解析为dict，无Schema验证")
print("2. PydanticOutputParser + LCEL链：自动生成格式指令，解析为Pydantic对象，有类型验证")
print("3. with_structured_output()：最简洁，无需手动写格式指令，直接返回Pydantic对象 ⭐推荐")
print("\n选择建议：简单场景用方式3，需要在链中灵活组合时用方式2")
