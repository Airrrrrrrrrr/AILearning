# LangChain学习Todo清单

> 每周约10小时，总待学习量约56-69h（含复习），预计6-7周完成
>
> ✅ = 已完成 | ⏭️ = 已跳过 | 🔲 = 待学习 | 🔄 = 复习

---

## 阶段一：AI大模型基础

- [x] LLM概念 / 主流模型 | ⏰ — | 📊 ⭐⭐ | 理解大模型本质是学习一切上层应用的先决条件
- [ ] ⏭️ Token和上下文窗口 | ⏰ — | 📊 ⭐⭐ | 日常使用中会自然理解，后续RAG也会涉及
- [x] Prompt Engineering | ⏰ — | 📊 ⭐⭐⭐ | 已在001~004文件中实践
- [ ] ⏭️ OpenAI API | ⏰ — | 📊 ⭐⭐ | API调用模式通用，需用时再学
- [x] 国产模型API / API参数配置 | ⏰ — | 📊 ⭐⭐ | model_config.py 已完成DeepSeek配置
- [ ] ⏭️ 错误处理（API层） | ⏰ — | 📊 ⭐⭐ | 当前聚焦核心功能
- [x] Python语法 / 常用库 | ⏰ — | 📊 ⭐⭐ | 整个项目使用Python 3.12
- [x] 异步编程 | ⏰ 1.5h | 📊 ⭐⭐⭐ | 阶段二中结合流式输出一起学 async/await 2026年5月30日 16点30分
- [x] 🔄 阶段一复习 | ⏰ 1h | 📊 — | 快速回顾已学内容，建立完整认知框架

> 💡 学习心得
>
> （完成本阶段后填写）

---

## 阶段二：LangChain核心概念

- [x] LangChain架构 / 安装配置 | ⏰ — | 📊 ⭐⭐ | pyproject.toml 已配置
- [x] LLM接口 / Chat Models / 模型参数 | ⏰ — | 📊 ⭐⭐ | 001文件已使用 ChatDeepSeek
- [x] 流式输出 | ⏰ — | 📊 ⭐⭐⭐ | helper.py 自定义流式打印
- [x] PromptTemplate / ChatPromptTemplate | ⏰ — | 📊 ⭐⭐ | 002、003文件已完成
- [x] Few-shot Prompts / Prompt组合 | ⏰ — | 📊 ⭐⭐⭐ | 003(MessagesPlaceholder)、004文件
- [x] OutputParser / JSON解析 | ⏰ — | 📊 ⭐⭐⭐ | 005文件 StrOutputParser, JsonOutputParser
- [x] 自定义Chain / RunnableLambda | ⏰ — | 📊 ⭐⭐⭐ | 005管道符、006 RunnableLambda/Passthrough
- [x] StructuredOutputParser / Pydantic解析器 | ⏰ 2.5h | 📊 ⭐⭐ | 生产环境刚需，RAG和Agent都依赖结构化输出
- [x] Stream与异步编程结合 | ⏰ 1.5h | 📊 ⭐⭐⭐ | 已有流式基础，补上 astream_events 支持并发 2026年5月30日 16点30分
- [ ] ⏭️ LLMChain / SequentialChain / RouterChain | ⏰ — | 📊 ⭐⭐⭐ | 新版已用管道符和LCEL替代
- [x] 🔄 阶段二复习 | ⏰ 1h | 📊 — | 重点巩固 Prompt/Chain/Parser，确保基础扎实

> 💡 学习心得
>
> （完成本阶段后填写）

---

## 阶段三：文档处理和RAG

- [ ] Document Loaders（PDF/文本/网页爬取） | ⏰ 2h | 📊 ⭐⭐ | RAG入口，没有文档加载就没有后续一切
- [ ] Text Splitters（字符/语义分割） | ⏰ 3h | 📊 ⭐⭐⭐ | 分割策略直接影响检索质量，RAG调优核心
- [ ] Embeddings + 向量存储 Chroma | ⏰ 3h | 📊 ⭐⭐⭐ | 语义搜索基石，Chroma零配置快速上手
- [ ] FAISS / Pinecone（大规模+云方案） | ⏰ 2h | 📊 ⭐⭐⭐ | FAISS应对大规模，Pinecone了解即可
- [ ] Retrievers + 检索优化（MMR/多路召回/重排序） | ⏰ 3h | 📊 ⭐⭐⭐⭐ | 检索质量决定RAG天花板，面试高频考点
- [ ] RetrievalQA / ConversationalRetrievalChain | ⏰ 3h | 📊 ⭐⭐⭐ | RAG端到端管线，阶段六实战预演
- [ ] 🔄 阶段三复习 | ⏰ 2h | 📊 — | 内容最多，需重点消化检索优化和管道串联

> 💡 学习心得
>
> （完成本阶段后填写）

---

## 阶段四：Agent和工具调用

- [ ] Agent概念与执行流程（ReAct循环） | ⏰ 2h | 📊 ⭐⭐⭐ | AI自主决策的核心范式
- [ ] Tools / 自定义工具 | ⏰ 4h | 📊 ⭐⭐⭐ | Agent的"手脚"，让LLM调用API、数据库、代码
- [ ] ReAct Agent 实战 | ⏰ 3h | 📊 ⭐⭐⭐⭐ | 最成熟的Agent模式，面试必问
- [ ] Plan-and-Execute 高级Agent | ⏰ 3h | 📊 ⭐⭐⭐⭐⭐ | 复杂任务拆解，AI应用前沿
- [ ] 多Agent协作 | ⏰ 2h | 📊 ⭐⭐⭐⭐⭐ | 构建AI团队的基础
- [ ] 🔄 阶段四复习 | ⏰ 2h | 📊 — | Agent概念密集，ReAct和工具设计需反复理解

> 💡 学习心得
>
> （完成本阶段后填写）

---

## 阶段五：记忆管理

- [x] InMemoryChatMessageHistory / 内存多轮对话 | ⏰ — | 📊 ⭐⭐ | 007文件已完成
- [x] FileChatMessageHistory / 文件持久化长期记忆 | ⏰ — | 📊 ⭐⭐⭐ | 008文件已完成
- [ ] ConversationSummaryMemory（自动压缩历史） | ⏰ 2h | 📊 ⭐⭐ | 长对话防Token爆炸的必备方案
- [ ] VectorStoreMemory（向量长期记忆） | ⏰ 2h | 📊 ⭐⭐⭐⭐ | 结合RAG让Agent记住海量历史
- [ ] 🔄 阶段五复习 | ⏰ 1h | 📊 — | 记忆管理相对轻量，快速串联三种记忆方案

> 💡 学习心得
>
> （完成本阶段后填写）

---

## 阶段六：项目实战

- [ ] 文档问答系统（上传PDF→智能问答→来源引用） | ⏰ 6h | 📊 ⭐⭐⭐⭐ | 融合阶段三，简历最有分量的RAG项目
- [ ] Agent应用（搜索+分析+总结全链路） | ⏰ 6h | 📊 ⭐⭐⭐⭐ | 融合阶段四，面试展示价值极高
- [ ] RAG知识库 企业级综合项目 | ⏰ 6h | 📊 ⭐⭐⭐⭐⭐ | RAG+Agent+Memory完整融合，求职核心作品
- [ ] 🔄 阶段六复习 | ⏰ 2h | 📊 — | 三个实战项目需整体复盘，梳理技术栈和踩坑记录

> 💡 学习心得
>
> （完成本阶段后填写）

---

## 阶段七：求职备战

- [ ] LangChain基础面试题（Chain/Memory/Prompt设计模式） | ⏰ 2h | 📊 ⭐⭐ | 体现扎实基本功
- [ ] RAG面试题（召回率/分块策略/幻觉处理） | ⏰ 3h | 📊 ⭐⭐⭐⭐ | RAG岗位必问，准备好就脱颖而出
- [ ] Agent面试题（ReAct原理/工具设计/安全） | ⏰ 3h | 📊 ⭐⭐⭐⭐ | 当前最热方向，深挖设计思路和调试经验
- [ ] 🔄 阶段七复习 | ⏰ 1h | 📊 — | 面试题梳理后查漏补缺，模拟自问自答

> 💡 学习心得
>
> （完成本阶段后填写）

---

## 总览

| 阶段 | 新学时长 | 复习时长 | 合计 | 进度 |
|------|----------|----------|------|------|
| 阶段一 大模型基础 | 1.5h | 1h | 2.5h | ✅ 基本完成 + 跳过不必要项 |
| 阶段二 核心概念 | 4h | 1h | 5h | 80% |
| 阶段三 文档处理和RAG | 16h | 2h | 18h | 0% |
| 阶段四 Agent和工具调用 | 14h | 2h | 16h | 0% |
| 阶段五 记忆管理 | 4h | 1h | 5h | 50% |
| 阶段六 项目实战 | 18h | 2h | 20h | 0% |
| 阶段七 求职备战 | 8h | 1h | 9h | 0% |
| **合计** | **65.5h** | **10h** | **75.5h** | — |

> **建议学习顺序：** 阶段一复习 → 阶段二补充 → 阶段三 → 阶段五补充 → 阶段四 → 阶段六 → 阶段七
