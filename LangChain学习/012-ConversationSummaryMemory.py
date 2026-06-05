"""
=== 012 - ConversationSummaryMemory（对话摘要记忆） ===

【学习目标】
1. 理解 Token 爆炸问题及其解决方案
2. 掌握 ConversationSummaryMemory 自动压缩长对话历史
3. 将 SummaryMemory 集成到 LCEL 链中实现多轮对话

【核心知识点】
- ConversationSummaryMemory：
  - 当对话历史超过 max_token_limit 时，自动调用 LLM 生成历史摘要
  - 只保留摘要 + 最近几轮对话，大幅减少 Token 消耗
  - 底层使用 ConversationSummaryBufferMemory（langchain 社区版）
- 对比三种记忆方案的场景：
  | 方案 | 优点 | 缺点 |
  |------|------|------|
  | 全量历史（007） | 不丢失信息 | Token 爆炸 |
  | 截断历史 | 简单 | 丢失早期上下文 |
  | SummaryMemory | 保留关键信息，省 Token | 摘要可能遗漏细节 |

【练习步骤】
1. 用 ConversationSummaryMemory 创建记忆实例，指定 llm 用于生成摘要
2. 模拟长对话（10+ 轮），观察 summary 何时触发、内容变化
3. 将 SummaryMemory 与 FileChatMessageHistory 结合，实现持久化+自动摘要
4. 用 prompt | model 链 + memory 实现带记忆的对话循环

【预期产出】
- 长对话中 SummaryMemory 的摘要对比输出
- 持久化 + 摘要的完整对话链

【提示】
- 新版 langchain 中 SummaryMemory 的导入路径可能在 langchain.memory
- 摘要生成的 llm 可以用同一个 ChatDeepSeek 实例
- 结合 FileChatMessageHistory 时：history = FileChatMessageHistory(path); memory = SummaryMemory(chat_memory=history, llm=model)
- 用 memory.load_memory_variables({}) 查看当前记忆状态
"""
