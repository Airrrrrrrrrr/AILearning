# LangChain Retriever 学习笔记

## 环境准备

```bash
# 需要 Python 3.8+
pip install langchain langchain-openai langchain-community faiss-cpu rank_bm25 numpy

# 设置 OpenAI API Key
export OPENAI_API_KEY="sk-xxx"
# 或 Windows PowerShell:
# $env:OPENAI_API_KEY = "sk-xxx"
```

---

## 一、核心概念：as_retriever()

### 1.1 什么是 Retriever

Retriever 是 LangChain 的标准检索接口，用于从数据源中返回与查询相关的 `Document` 列表。

```
VectorStore.as_retriever() → VectorStoreRetriever (Runnable)
```

### 1.2 与 similarity_search() 的区别

| 对比项 | `similarity_search()` | `as_retriever()` |
|---|---|---|
| 返回类型 | `List[Document]` | `VectorStoreRetriever` |
| 接口类型 | 普通方法 | Runnable（LCEL） |
| 异步支持 | `asimilarity_search()` | `ainvoke()` |
| 链式调用 | 不支持 | 支持 `\|` 管道 |
| 批处理 | 不支持 | `batch()` |
| 流式 | 不适用 | `stream()` |
| 使用场景 | 简单检索 | RAG 管道、生产系统 |

### 1.3 三种 search_type

```python
# 默认：纯相似度排序
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# MMR：平衡相关性与多样性
retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 3, "fetch_k": 10, "lambda_mult": 0.5})

# 相似度阈值过滤
retriever = vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 5, "score_threshold": 0.7})
```

---

## 二、similarity（默认策略）

### 原理
按余弦相似度 / L2 距离排序，返回 Top-K 最相似的文档。

### 参数
- `k`：返回文档数量（默认 4）

### 适用场景
- 通用检索
- 语料差异度高的场景

### 示例
```python
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
results = retriever.invoke("什么是机器学习？")
```

---

## 三、MMR（最大边际相关性）

### 原理
每次选择文档时，同时考虑：
1. **与查询的相关性**（相似度）
2. **与已选文档的差异性**（避免冗余）

公式：
```
MMR(d) = λ × Sim(d, q) - (1-λ) × max[Sim(d, d_selected)]
```

### 参数
| 参数 | 含义 | 建议值 |
|---|---|---|
| `k` | 最终返回数量 | 3-5 |
| `fetch_k` | 初始候选集大小 | >= k，建议 2~3x k |
| `lambda_mult` | 相关性 vs 多样性权重 | 0.5（默认），0.0=纯多样，1.0=纯相关 |

### lambda_mult 调优指南

| 值 | 效果 | 适用场景 |
|---|---|---|
| 0.0 | 最大多样性 | 探索性查询、概览 |
| 0.3 | 偏多样性 | 多角度分析 |
| 0.5 | 平衡 | 通用场景 |
| 0.8 | 偏相关性 | 精确回答 |
| 1.0 | 纯相关性（等同 similarity） | 不需要多样性 |

### 适用场景
- 语料中有大量语义重复的文档
- 需要多角度回答用户问题
- 避免返回"说的都是同一件事"的文档

---

## 四、similarity_score_threshold

### 原理
在 similarity 的基础上，只返回相似度分数 >= threshold 的文档。

### 参数
| 参数 | 含义 | 注意 |
|---|---|---|
| `k` | 最大返回数量 | 实际返回可能 < k |
| `score_threshold` | 最低相似度（0~1） | 不同向量库的分数归一化方式不同 |

### 不同向量库的分数

| 向量库 | 底层度量 | 分数含义 |
|---|---|---|
| FAISS (L2) | 欧氏距离 | 越小越好，LangChain 会转为 0~1 |
| ChromaDB | 余弦相似度 | 0~1，越大越好 |
| Pinecone | 余弦相似度 | 0~1 |
| Milvus | 可配置 | 取决于 metric |

### 最佳实践
1. **先用 `similarity_search_with_score()` 查看分数分布**
2. 根据分布选择合适的 threshold
3. **务必设置 fallback 策略**处理空结果

```python
# 查看分数分布
results = vector_store.similarity_search_with_score("查询", k=20)
for doc, score in results:
    print(f"score={score:.4f} | {doc.page_content[:40]}")

# 设置 threshold
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 5, "score_threshold": 0.7}
)

# Fallback
results = retriever.invoke(query)
if not results:
    results = fallback_retriever.invoke(query)
```

---

## 五、多路召回策略

### 5.1 为什么需要多路召回

| 检索方式 | 擅长 | 不擅长 |
|---|---|---|
| 语义检索 | 同义词、概念理解 | 精确关键词、专有名词 |
| BM25 关键词 | 精确匹配、专有名词 | 同义词、语义关联 |

**单一检索方式存在盲区**，多路召回互补提升召回率。

### 5.2 架构流程

```
  Query
   │
   ├──────────────┐
   │              │
   ▼              ▼
  BM25          语义检索
  (关键词)      (FAISS/Chroma)
   │              │
   └──────┬───────┘
          │
          ▼
     合并去重
     (Union / RRF)
          │
          ▼
     重排序 Rerank
     (交叉编码器)
          │
          ▼
      Top-K 结果
```

### 5.3 合并策略

| 策略 | 方法 | 特点 |
|---|---|---|
| Union | 简单去重合并 | 最简单 |
| RRF (Reciprocal Rank Fusion) | 按排名倒数加权 | 考虑排序位置 |
| 加权分数 | 线性组合各路分数 | 需调权重 |

### 5.4 Rerank 方案

| 方案 | 特点 | 适用场景 |
|---|---|---|
| Cohere Rerank | API 调用，效果好 | 快速集成 |
| BGE-Reranker | 本地部署，中文优秀 | 中文场景 |
| Jina Reranker | 轻量高效 | 多语言 |
| 交叉编码器 | 精度高、速度慢 | 小规模精排 |

### 5.5 生产建议
- BM25 + 语义检索是标配组合
- 候选集建议 20-50 条，Rerank 后取 3-5 条
- Rerank 是提升最终效果的关键步骤
- 考虑用 RRF 替代简单 Union 获得更稳定的合并效果

---

## 六、文件索引

| 文件 | 内容 | 运行命令 |
|---|---|---|
| `01_as_retriever_similarity.py` | 基础检索 + LCEL 链 | `python 01_as_retriever_similarity.py` |
| `02_as_retriever_mmr.py` | MMR 多样性检索 | `python 02_as_retriever_mmr.py` |
| `03_as_retriever_threshold.py` | 相似度阈值过滤 | `python 03_as_retriever_threshold.py` |
| `04_multi_retrieval.py` | 多路召回 + Rerank | `python 04_multi_retrieval.py` |

---

## 七、常见问题 FAQ

**Q: fetch_k 设多大合适？**
A: 至少 >= k，建议设为 k 的 2-3 倍。太大会影响性能，太小无法发挥 MMR 的多样性优势。

**Q: threshold 设多少合适？**
A: 没有固定值，取决于向量库和 embedding 模型。建议先跑 `similarity_search_with_score` 查看分数分布再决定。

**Q: Retriever 和 Tool 有什么区别？**
A: Retriever 返回 Document 列表，Tool 是给 Agent 调用的函数。Retriever 可以包装成 Tool 供 Agent 使用。

**Q: 多路召回一定比单路好吗？**
A: 召回率一定更高，但如果不做 Rerank，最终精度可能反而下降。**多路召回 + Rerank** 是推荐组合。
