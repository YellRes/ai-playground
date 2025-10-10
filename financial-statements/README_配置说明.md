# 财务报表分析智能体 - 完整配置说明

## 📌 重要说明：为什么使用 `langchain_openai`？

### 您的疑问
> "我提供的是 DeepSeek 的 key 但是这边使用了 openai 该如何修改"

### 答案
**✅ 代码是正确的，不需要修改导入部分！**

```python
from langchain_openai import ChatOpenAI  # ✅ 这样写是对的！
```

**原因：**
1. **DeepSeek 提供 OpenAI 兼容的 API**：DeepSeek 实现了与 OpenAI 相同的 API 接口规范
2. **只需更改 API 地址**：通过设置 `openai_api_base="https://api.deepseek.com"` 即可
3. **使用 DeepSeek API Key**：使用您的 DeepSeek API 密钥，不需要 OpenAI 密钥

**代码配置示例：**
```python
llm = ChatOpenAI(
    model="deepseek-chat",              # DeepSeek 模型
    openai_api_key=DEEPSEEK_API_KEY,   # 您的 DeepSeek API Key
    openai_api_base="https://api.deepseek.com",  # DeepSeek API 地址
    temperature=0.7,
)
```

这就像使用同一个手机 APP（langchain_openai），但连接到不同的服务器（DeepSeek 而不是 OpenAI）。

---

## 🚀 快速开始

### 1. 安装依赖
```bash
cd langchain/financial-statements
pip install -r requirements.txt
```

### 2. 配置 API 密钥

创建 `.env` 文件（在 `langchain/financial-statements/` 目录下）：

```bash
# .env 文件内容
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

**获取 API 密钥：**
1. 访问 https://platform.deepseek.com/
2. 注册/登录账号
3. 在控制台创建 API 密钥
4. 复制密钥到 `.env` 文件

### 3. 测试配置

**强烈推荐先运行测试脚本：**

```bash
python test_api.py
```

这会检查：
- ✅ API Key 是否正确配置
- ✅ Chat API 是否可用
- ⚠️  Embeddings API 是否支持

### 4. 运行程序

```bash
# 基础对话示例
python index.py

# 交互式对话模式（推荐）
python index.py interactive

# PDF 分析示例（需要 Embeddings 支持）
python index.py pdf
```

---

## 🔧 常见问题解决

### 问题 1：认证失败 (401 Error)

**错误信息：**
```
openai.AuthenticationError: Error code: 401 - {'error': {'message': 'Authentication Fails...'}}
```

**可能原因和解决方法：**

#### ✅ 检查 .env 文件是否存在
```bash
# Windows PowerShell
Test-Path .env

# 如果返回 False，创建 .env 文件：
New-Item -Path .env -ItemType File
```

#### ✅ 检查 API Key 格式
- 确保没有多余的空格
- 确保没有引号
- 格式应该是：`DEEPSEEK_API_KEY=sk-xxxxx`

#### ✅ 验证 API Key 有效性
```bash
python test_api.py
```

#### ✅ 检查 API Key 是否过期
- 登录 https://platform.deepseek.com/
- 查看 API Key 状态
- 必要时重新生成新的密钥

---

### 问题 2：Embeddings API 不支持

**错误信息：**
```
❌ 创建向量索引失败: ...
```

**说明：**
DeepSeek 可能不支持 Embeddings API（用于 PDF 向量化搜索）

**解决方案：**

#### 方案 A：使用 HuggingFace 本地模型（推荐）

1. 安装依赖：
```bash
pip install sentence-transformers
```

2. 修改 `index.py` 中的 embeddings 部分：
```python
# 替换这部分代码（在 load_financial_pdf 函数中）
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
```

#### 方案 B：使用 OpenAI Embeddings

1. 获取 OpenAI API Key（需要额外注册）
2. 在 `.env` 中添加：
```bash
DEEPSEEK_API_KEY=sk-deepseek-xxxxx
OPENAI_API_KEY=sk-openai-xxxxx
```

3. 修改代码使用 OpenAI Embeddings

#### 方案 C：不使用 PDF 向量检索

- 基础对话功能不受影响
- 仍然可以使用 `extract_financial_data` 工具提取数据
- 只是无法使用 `search_financial_info` 进行向量检索

---

### 问题 3：废弃警告

**警告信息：**
```
LangGraphDeprecatedSinceV10: create_react_agent has been moved to langchain.agents
```

**说明：**
这只是一个警告，不影响程序运行。LangGraph 团队正在重构 API。

**如何消除警告（可选）：**
代码已经使用最新的方式，这个警告会在未来版本中自动消失。暂时可以忽略。

---

## 📁 项目文件说明

```
financial-statements/
├── index.py                   # 主程序文件
├── test_api.py               # API 配置测试脚本（新增）
├── requirements.txt          # Python 依赖包列表
├── .env                      # 环境配置文件（需要手动创建）
├── 环境配置说明.md           # 详细配置说明
├── README_配置说明.md        # 本文件
└── 600006_20250830_WOQW.pdf # 示例财务报表
```

---

## 🎯 功能说明

### 基础财务分析功能
- ✅ 计算财务比率（ROE、ROA、流动比率等）
- ✅ 分析盈利能力
- ✅ 分析流动性和偿债能力
- ✅ 分析杠杆和资本结构

### PDF 分析功能（需要 Embeddings 支持）
- ⚠️  加载 PDF 财务报表
- ⚠️  向量检索特定信息
- ✅ 提取财务数据（使用正则表达式，不需要 Embeddings）

---

## 💡 使用建议

### 推荐工作流程

1. **测试 API 连接**
   ```bash
   python test_api.py
   ```

2. **从交互式模式开始**
   ```bash
   python index.py interactive
   ```
   示例对话：
   ```
   👤 您: 你好，请介绍一下你能做什么？
   
   👤 您: 假设一家公司营业收入1000万，净利润150万，总资产2000万，请分析盈利能力
   ```

3. **如果 Embeddings API 不支持，使用文本提取**
   - 不要使用 `load_financial_pdf` 工具
   - 直接使用 `extract_financial_data` 工具
   - 或手动提供财务数据进行分析

---

## 📞 获取帮助

如果遇到问题：

1. **查看测试脚本输出**
   ```bash
   python test_api.py
   ```

2. **检查 API Key 配置**
   - 确认 `.env` 文件存在
   - 确认 API Key 格式正确
   - 确认 API Key 有效且未过期

3. **查看详细错误信息**
   - 运行程序时会显示具体错误
   - 根据错误信息查找对应的解决方案

4. **参考官方文档**
   - [DeepSeek 文档](https://platform.deepseek.com/docs)
   - [LangChain 文档](https://python.langchain.com/)

---

## ✅ 总结

### 关键要点
1. ✅ **使用 `langchain_openai` 是正确的**，因为 DeepSeek 兼容 OpenAI API
2. ✅ **只需要 DeepSeek API Key**，不需要 OpenAI 密钥
3. ✅ **通过 `openai_api_base` 切换到 DeepSeek 服务器**
4. ⚠️  **Embeddings 可能不支持**，但不影响核心功能

### 快速诊断
```bash
# 1. 测试配置
python test_api.py

# 2. 如果测试通过，运行主程序
python index.py interactive

# 3. 享受 AI 财务分析！
```

祝您使用愉快！🎉

