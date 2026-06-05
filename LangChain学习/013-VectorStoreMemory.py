"""
=== 013 - VectorStoreMemory（向量长期记忆） ===

【学习目标】
1. 理解向量记忆与 RAG 的关系——把对话历史当作文档库检索
2. 掌握 VectorStoreRetrieverMemory 的构建与使用
3. 将向量记忆集成到 Chain 或 Agent 中

【核心知识点】
- VectorStoreRetrieverMemory：
  - 将每轮对话存储为向量（User: xxx + AI: xxx），存入 Chroma
  - 用户新提问时，从历史中检索最相关的过去对话片段
  - 不是返回"全部历史"，而是返回"与当前问题最相关的历史"
- 与 RAG 的类比：
  | | RAG | VectorStoreMemory |
  |------|-----|-------------------|
  | 存入内容 | 外部文档 | 对话历史 |
  | 检索目的 | 找到相关知识 | 找到相关上下文 |
  | 本质 | 外部知识增强 | 内部记忆增强 |
- 与 ConversationSummaryMemory 对比：SummaryMemory 是"压缩"，VectorStoreMemory 是"选择性提取"

【练习步骤】
1. 用 Chroma 创建向量库，将对话历史逐条向量化存入
2. 用 VectorStoreRetrieverMemory 包装向量库和检索器
3. 模拟一段长对话（涵盖多个话题），验证"根据当前问题检索到最相关历史"
4. 将 VectorStoreMemory 集成到对话链中，对比有无向量记忆的回答差异

【预期产出】
- VectorStoreMemory 的检索效果展示
- 集成向量记忆的对话链示例

【提示】
- 复用已有的 BGEZhEmbeddings + Chroma 知识（RAG学习/03）
- 存入的历史格式建议为 "User: {input}\nAI: {output}"
- VectorStoreRetrieverMemory 需要传入 retriever（通过 as_retriever() 创建）
- 将 memory 注入 prompt 的 {history} 变量中
- 测试时先聊"电影"话题，再聊"天气"话题，然后回到"电影"——观察记忆检索是否精准
"""
