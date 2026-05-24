## ChatPromptTemplate 各方法详解

### 1. `from_messages` — 类方法（创建模板）

从**消息列表**创建模板。消息可以是三种形式：

```python
ChatPromptTemplate.from_messages([
    # ① 元组形式：("角色", "文本") — 文本会被解析为模板
    ("system", "你是{role}"),
    ("human", "{question}"),

    # ② Message 对象：静态内容，❌不会解析模板变量
    SystemMessage(content="你是{role}"),  # {role} 是字面量，不会被替换！

    # ③ MessagePromptTemplate：可以解析变量
    HumanMessagePromptTemplate.from_template("{question}"),
])
```

**关键区别**：元组中的字符串会自动解析 `{}` 变量；`HumanMessage(content="...")` 是**静态内容**，里面的 `{words}` 永远不会被替换。这就是你之前遇到注入失败的原因。

---

### 2. `from_template` — 类方法（创建模板）

从**单个字符串**创建模板，自动包装为 `("human", template)` ：

```python
prompt = ChatPromptTemplate.from_template("你觉得{things}怎么样？")
# 等价于：
prompt = ChatPromptTemplate.from_messages([("human", "你觉得{things}怎么样？")])
```

---

### 3. `format_messages` — 实例方法（格式化输出）

传入变量 → 返回 **`List[Message]`** 对象列表，可以直接喂给模型：

```python
messages = chat_prompt.format_messages(role="企鹅老大", question="罐头在哪？")
# 返回: [SystemMessage(...), HumanMessage(...), ...]
response = model.invoke(messages)
```

---

### 4. `format_prompt` — 实例方法（格式化输出）

传入变量 → 返回 **`ChatPromptValue`** 对象（包装了 messages 列表）：

```python
prompt_value = chat_prompt.format_prompt(role="企鹅老大", question="罐头在哪？")
# prompt_value.messages  # 获取消息列表
# prompt_value.to_string()  # 转成字符串
```

和 `format_messages` 的区别：返回值是 `ChatPromptValue` 而非裸 `list`，多了一层封装。

---

### 5. `format` — 实例方法（格式化输出）

传入变量 → 返回**纯字符串**（将所有消息拼接成一个字符串）：

```python
text = chat_prompt.format(role="老大", question="罐头呢？")
# 返回: "System: 你是老大\nHuman: 罐头呢？"
```

很少用在 Chat 场景，因为 chat model 通常需要结构化的 message list。

---

### 6. `invoke` — 实例方法（LCEL 入口）

LCEL（LangChain Expression Language）统一接口，等价于 `format_prompt`：

```python
prompt_value = chat_prompt.invoke({"role": "老大", "question": "罐头呢？"})
```

---

### 总结对比表

| 方法 | 类型 | 输入 | 输出 | 用途 |
|------|------|------|------|------|
| `from_messages` | 类方法 | 消息列表 | `ChatPromptTemplate` | **创建**多轮对话模板 |
| `from_template` | 类方法 | 单个字符串 | `ChatPromptTemplate` | **创建**单轮对话模板 |
| `format_messages` | 实例方法 | 变量值 | `List[Message]` | **格式化**，直接给模型 |
| `format_prompt` | 实例方法 | 变量值 | `ChatPromptValue` | **格式化**，包装后的消息 |
| `format` | 实例方法 | 变量值 | `str` | **格式化**为纯文本 |
| `invoke` | 实例方法 | `dict` | `ChatPromptValue` | LCEL 标准入口 |

最常用的组合：**`from_messages` + `invoke`**（或 `format_messages`）→ 直接喂给模型。