"""
=== 05 - RetrievalQA 与对话链 ===

【学习目标】
1. 掌握 create_retrieval_chain() 构建端到端 RAG 问答链
2. 使用 create_history_aware_retriever 处理多轮对话中的指代消解
3. 理解 create_stuff_documents_chain 将检索文档拼入 prompt
4. 实现带来源引用的回答

【核心知识点】
- RAG 链路：用户问题 → 检索器召回文档 → 拼入 Prompt → LLM 生成回答
- create_stuff_documents_chain(prompt, model)：
  将检索到的多个 Document 塞进 prompt 的 {context} 变量
- create_retrieval_chain(retriever, combine_docs_chain)：
  串联"检索 → 整合文档 → 生成回答"的完整链
- create_history_aware_retriever(model_for_history, retriever, prompt)：
  将用户的追问改写为独立问题后再检索（解决"它呢？""那个"等指代问题）
- 来源引用：从 Document.metadata 中提取来源信息附加到最终回答

【练习步骤】
1. 用 create_stuff_documents_chain 构建文档拼接链
2. 用 create_retrieval_chain 构建完整 RAG 问答链，测试单轮问答
3. 用 create_history_aware_retriever 处理多轮对话追问
4. 在 prompt 中要求模型标注引用来源，从 Document.metadata 提取信息

【预期产出】
- 完整的 RAG 问答链代码
- 多轮对话中能正确处理指代消解
- 回答带来源引用

【提示】
- 复用 03 的 Chroma + BGEZhEmbeddings
- ChatPromptTemplate 中 {context} 和 {input} 是内置占位符
- create_history_aware_retriever 需要单独的 ChatModel 实例（可以复用同一个）
- 来源引用可在 Prompt 中要求模型用 [来源: title, year] 格式标注
"""
