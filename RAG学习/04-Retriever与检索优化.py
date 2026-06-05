"""
=== 04 - Retriever 与检索优化 ===

【学习目标】
1. 掌握 vector_store.as_retriever() 从向量库创建检索器
2. 理解 MMR（最大边际相关性）避免冗余结果
3. 掌握 similarity_score_threshold 相似度阈值过滤
4. 了解多路召回策略的架构思路

【核心知识点】
- as_retriever()：将 vector_store 包装为标准 Retriever 接口
  - search_type="similarity"：纯相似度排序（默认）
  - search_type="mmr"：平衡相关性与多样性，fetch_k > k
  - search_type="similarity_score_threshold"：仅返回分数 >= threshold 的结果
- Retriever 与 vector_store.similarity_search() 的区别：
  - Retriever 是 Runnable 接口，可嵌入 LCEL 链中
  - 直接 search 返回 Document 列表，Retriever 支持异步 invoke
- 多路召回：关键词检索（BM25）+ 语义检索 → 合并去重 → 重排序（Rerank）

【练习步骤】
1. 基于 02/03 已有的 Chroma 向量库，用 as_retriever() 创建 3 种检索器
2. 对比 similarity / mmr / score_threshold 三者的返回结果差异
3. 用 retriever.invoke() 检索，再用 RunnableLambda 注入到 prompt 中（模拟"检索后问答"）
4. 尝试 mmr 的 fetch_k=10, k=3，观察多样性提升效果

【预期产出】
- 三种检索器的对比输出
- Retriever + Prompt + Model 的 LCEL 链示例

【提示】
- 复用 03 已持久化的 chroma_langchain_db，直接 Chroma(...) 加载
- mmr 的 lambda_mult=0.5 是默认平衡点，越小越多样化，越大越精准
- similarity_score_threshold 需要 embedding 函数 normalize 过才能用 0~1 的阈值
- filter 参数在 as_retriever() 的 search_kwargs 中传入：search_kwargs={"filter": {...}}
"""
# -*- coding: utf-8 -*-
# @Time    : 2026/5/31 16:31
# @Author  : 20962
# @Description  :
import os
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer


class BGEZhEmbeddings(Embeddings):
    def __init__(self, model_path: str):
        self.model = SentenceTransformer(model_path)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.model.encode(text, normalize_embeddings=True).tolist()


dir_path = r"C:\Users\Asus\.cache\huggingface\hub\models--BAAI--bge-large-zh-v1.5"
embedding = BGEZhEmbeddings(model_path=os.path.abspath(dir_path))
vector_store = Chroma(
    collection_name="movies",
    embedding_function=embedding,
    persist_directory=r"C:\Users\Asus\Desktop\个人\AILearning\RAG学习\chroma_langchain_db",
)

retriever = vector_store.as_retriever()
query = "爱情"
results = retriever.invoke(query)
print(type(results))
for i, doc in enumerate(results):
    print(f'[{i+1}] (title={doc.metadata['title']}) {doc.page_content}]')