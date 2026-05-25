# AILearning

个人 AI 学习项目，基于 LangChain + DeepSeek 大模型。

## 环境要求

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) 包管理器

### 安装 uv

```powershell
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

其他平台安装方式见 [uv 官方文档](https://docs.astral.sh/uv/getting-started/installation/)。

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Airrrrrrrrrr/AILearning.git
cd AILearning
```

### 2. 配置环境变量
在环境变量中添加你的DEEPSEEK_API_KEY键值对。
创建 `.env` 文件并写入 DeepSeek API Key（该文件已在 `.gitignore` 中忽略）：

```bash
DEEPSEEK_API_KEY=你的DeepSeek_API_Key
```

### 3. 安装依赖

```bash
uv sync
```

该命令会自动：
- 根据 `.python-version` 下载对应 Python 版本（如未安装）
- 创建虚拟环境并安装 `pyproject.toml` 中声明的依赖

### 4. 运行示例

```bash
# 运行单个学习脚本
uv run python "LangChain学习/001-DeepSeek云模型连接.py"

# 或者激活虚拟环境后直接运行
.venv\Scripts\activate       # Windows
python "LangChain学习/001-DeepSeek云模型连接.py"
```

## 常用 uv 命令

| 命令 | 说明 |
|------|------|
| `uv sync` | 同步依赖，创建/更新虚拟环境 |
| `uv run python <脚本>` | 在项目环境中运行脚本 |
| `uv add <包名>` | 添加新依赖 |
| `uv remove <包名>` | 移除依赖 |
| `uv lock` | 更新锁定文件 |
