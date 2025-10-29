# 财务报表分析智能体 📊

基于 LangChain 和 DeepSeek 创建的智能财务分析助手，支持PDF财报解析和深度财务分析。

## 功能特性 ✨

### 1. PDF财报处理
- ✅ 加载PDF格式的财务报表
- ✅ 智能文本分割和向量索引
- ✅ 语义检索相关财务信息
- ✅ 自动提取关键财务数据

### 2. 财务分析工具
- 📈 **盈利能力分析**：ROA、ROE、利润率等
- 💰 **流动性分析**：流动比率、速动比率、现金比率
- 🏦 **杠杆分析**：资产负债率、利息保障倍数
- 🔢 **财务比率计算**：自定义比率计算

### 3. 智能交互
- 💬 对话式财务咨询
- 🧠 上下文记忆能力
- 🎯 自动选择合适的分析工具
- 📝 生成专业分析报告

## 安装依赖 📦

```bash
# 安装所需的Python包
pip install -r requirements.txt
```

主要依赖：
- `langchain` - LangChain框架
- `langgraph` - 图状态管理
- `langchain-openai` - OpenAI API集成
- `pypdf` - PDF解析
- `faiss-cpu` - 向量检索
- `python-dotenv` - 环境变量管理

## 配置环境 ⚙️

创建 `.env` 文件并配置DeepSeek API密钥：

```env
DEEPSEEK_API_KEY=your_api_key_here
```

## 使用方法 🚀

### 方式1：基础示例
运行预设的测试示例：

```bash
python index.py
```

### 方式2：PDF分析模式
分析PDF财务报表：

```bash
python index.py pdf
```

这将自动：
1. 加载 `600006_20250830_WOQW.pdf` 文件
2. 提取关键财务数据
3. 生成综合财务分析报告

### 方式3：交互式模式
进入对话式分析模式：

```bash
python index.py interactive
```

在交互模式中，你可以：
- 提供PDF文件路径进行分析
- 手动输入财务数据进行计算
- 询问财务相关问题
- 输入 `exit` 或 `quit` 退出
- 输入 `clear` 清除对话历史

## 使用示例 💡

### 1. 加载并分析PDF财报

```python
# 在交互模式中输入：
请加载并分析这个PDF文件：langchain/financial-statements/600006_20250830_WOQW.pdf
```

AI将自动：
- 加载PDF文件
- 提取所有关键财务指标
- 分析盈利能力、流动性和杠杆
- 生成综合分析报告

### 2. 检索特定信息

```python
# 在交互模式中输入：
从财报中找出关于营业收入的信息
```

### 3. 手动数据分析

```python
# 在交互模式中输入：
分析一家公司：营业收入1000万，净利润150万，总资产2000万
```

## 工具说明 🛠️

### PDF处理工具

#### `load_financial_pdf(pdf_path: str)`
加载PDF财务报表并创建向量索引

**参数：**
- `pdf_path`: PDF文件路径

**返回：** 加载状态和文档统计信息

#### `search_financial_info(query: str)`
从PDF中检索相关财务信息

**参数：**
- `query`: 查询内容（如"营业收入"、"资产负债表"）

**返回：** 检索到的相关文本片段

#### `extract_financial_data(data_type: str)`
自动提取特定的财务数据

**参数：**
- `data_type`: 数据类型
  - `'revenue'`: 营业收入
  - `'net_income'`: 净利润
  - `'total_assets'`: 总资产
  - `'total_liabilities'`: 总负债
  - `'equity'`: 股东权益
  - `'current_assets'`: 流动资产
  - `'current_liabilities'`: 流动负债
  - `'cash'`: 货币资金
  - `'all'`: 提取所有指标

**返回：** 提取的财务数据

### 财务分析工具

#### `calculate_financial_ratio(metric, numerator, denominator)`
计算财务比率

#### `analyze_profitability(revenue, net_income, total_assets)`
分析盈利能力

#### `analyze_liquidity(current_assets, current_liabilities, cash, inventory)`
分析流动性

#### `analyze_leverage(total_assets, total_liabilities, equity, interest_expense, ebit)`
分析杠杆和资本结构

## 技术架构 🏗️

```
┌─────────────────────────────────────────┐
│         用户交互界面 (CLI)              │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      LangGraph Agent (ReAct模式)        │
│   ┌──────────────────────────────────┐  │
│   │    DeepSeek LLM (deepseek-chat)  │  │
│   └──────────────────────────────────┘  │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐  ┌──▼───┐  ┌──▼────┐
│PDF工具│  │分析  │  │计算   │
│       │  │工具  │  │工具   │
└───┬───┘  └──────┘  └───────┘
    │
┌───▼─────────────────┐
│  PDF → Text         │
│  Text → Chunks      │
│  Chunks → Vectors   │
│  FAISS 向量存储     │
└─────────────────────┘
```

## 工作流程 🔄

1. **加载阶段**
   ```
   PDF文件 → PyPDFLoader → 文本提取 → 文本分割 → 向量化 → FAISS索引
   ```

2. **检索阶段**
   ```
   用户查询 → 向量化 → 相似度搜索 → 返回相关片段
   ```

3. **分析阶段**
   ```
   财务数据 → Agent调用工具 → 计算分析 → 生成报告
   ```

## 自定义扩展 🔧

### 添加新的财务指标提取

在 `extract_financial_data` 函数中添加新的正则表达式模式：

```python
patterns = {
    # ... 现有模式
    'new_metric': [
        r'新指标名称[：:]\s*([\d,，.]+)',
    ],
}
```

### 添加新的分析工具

创建新的 `@tool` 装饰的函数：

```python
@tool
def analyze_custom(param1: float, param2: float) -> str:
    """
    自定义分析工具
    
    Args:
        param1: 参数1说明
        param2: 参数2说明
    
    Returns:
        分析结果
    """
    # 实现分析逻辑
    return "分析结果"
```

然后在 `create_financial_agent()` 中添加到工具列表：

```python
tools = [
    # ... 现有工具
    analyze_custom,
]
```

## 注意事项 ⚠️

1. **API密钥**：确保正确配置 DeepSeek API 密钥
2. **PDF格式**：支持标准的PDF格式，OCR扫描件可能需要额外处理
3. **数据准确性**：自动提取的数据建议人工复核
4. **向量模型**：默认使用 DeepSeek 的 embedding 模型，确保API支持
5. **内存使用**：大型PDF文件可能占用较多内存

## 故障排除 🔍

### 问题1：PDF加载失败
```
❌ 加载PDF文件失败: ...
```

**解决方案：**
- 检查文件路径是否正确
- 确认PDF文件格式正常
- 尝试重新下载PDF文件

### 问题2：向量化失败
```
❌ 检索失败: ...
```

**解决方案：**
- 检查 DeepSeek API 密钥配置
- 确认 API 服务可用
- 检查网络连接

### 问题3：数据提取不准确

**解决方案：**
- 检查PDF中的数字格式
- 调整正则表达式模式
- 使用 `search_financial_info` 手动检索

## 示例输出 📄

```
============================================================
📝 问题: 请加载并分析这个PDF文件：600006_20250830_WOQW.pdf
============================================================

🤖 AI: 
✅ 成功加载PDF文件！
- 文档页数: 45
- 文本块数: 128
- 已建立向量索引，可以开始查询分析

📊 提取的财务数据：
- 营业收入: 1,234,567,890.00
- 净利润: 123,456,789.00
- 总资产: 9,876,543,210.00
...

📊 盈利能力分析报告：
- 利润率: 10.00%
- 总资产收益率(ROA): 1.25%
...
```

## 许可证 📄

MIT License

## 贡献 🤝

欢迎提交 Issue 和 Pull Request！

## 更新日志 📝

### v1.0.0 (2025-01-09)
- ✨ 初始版本发布
- ✅ 支持PDF财报解析
- ✅ 多种财务分析工具
- ✅ 交互式对话模式

