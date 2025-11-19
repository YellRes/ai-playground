# LangChain Memory 教程

这个目录包含了 LangChain 中四种主要 Memory 类型的完整示例和教程。

## 📚 教程内容

### 1. ConversationBufferMemory（基础缓冲内存）
**文件**: `01_buffer_memory.py`

**核心概念**: 保存所有完整的对话历史

**特点**:
- ✅ 信息完整，不丢失任何内容
- ✅ 实现简单，易于理解
- ❌ 内存会无限增长
- ❌ 可能超出 LLM 的 token 限制

**适用场景**: 短对话、开发测试阶段

---

### 2. ConversationBufferWindowMemory（窗口缓冲内存）
**文件**: `02_window_memory.py`

**核心概念**: 只保留最近的 K 轮对话

**特点**:
- ✅ 内存大小可控
- ✅ 不会超出 token 限制
- ❌ 会丢失早期对话
- ❌ 可能丢失重要上下文

**适用场景**: 长对话、客服问答

**关键参数**: `k=3` 表示保留最近 3 轮对话

---

### 3. ConversationSummaryMemory（摘要内存）
**文件**: `03_summary_memory.py`

**核心概念**: 使用 LLM 生成对话摘要

**特点**:
- ✅ 大幅压缩 token 数量
- ✅ 保留关键信息
- ❌ 需要额外的 LLM 调用（成本）
- ❌ 可能丢失细节

**适用场景**: 超长对话、会议纪要

**⚠️ 注意**: 需要 OpenAI API Key

---

### 4. ConversationSummaryBufferMemory（摘要缓冲内存）⭐ 推荐
**文件**: `04_summary_buffer_memory.py`

**核心概念**: 摘要 + 最近完整对话的组合

**特点**:
- ✅ 兼顾完整性和效率
- ✅ 保留近期完整上下文
- ✅ 保留早期关键信息
- ✅ Token 数量可控

**适用场景**: 生产环境、中长对话应用

**关键参数**: `max_token_limit=400` 控制何时开始总结

**⚠️ 注意**: 需要 OpenAI API Key

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install langchain langchain-openai
```

### 2. 设置 API Key（如果需要）

某些示例需要 OpenAI API Key：

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key"

# Windows CMD
set OPENAI_API_KEY=your-api-key

# Linux/Mac
export OPENAI_API_KEY=your-api-key
```

### 3. 运行示例

```bash
# 基础示例（不需要 API）
python 01_buffer_memory.py
python 02_window_memory.py

# 高级示例（需要 API）
python 03_summary_memory.py
python 04_summary_buffer_memory.py
```

---

## 📊 四种 Memory 类型对比表

| Memory 类型 | 保存内容 | Token 占用 | 需要 API | 适用场景 | 推荐指数 |
|------------|---------|-----------|---------|---------|---------|
| Buffer | 全部历史 | 无限增长 | ❌ | 短对话/测试 | ⭐⭐⭐ |
| Window | 最近 K 轮 | 固定大小 | ❌ | 长对话/客服 | ⭐⭐⭐⭐ |
| Summary | 摘要 | 压缩很多 | ✅ | 超长对话 | ⭐⭐⭐ |
| SummaryBuffer | 摘要+近期 | 可控 | ✅ | 生产环境 | ⭐⭐⭐⭐⭐ |

---

## 💡 学习建议

### 学习路径
1. **第一天**: 学习 `01_buffer_memory.py` - 理解基本概念
2. **第二天**: 学习 `02_window_memory.py` - 理解如何控制内存
3. **第三天**: 学习 `03_summary_memory.py` - 理解摘要机制
4. **第四天**: 学习 `04_summary_buffer_memory.py` - 理解最佳实践

### 实践建议
- 每个示例都有多个演示函数，建议逐个运行
- 尝试修改参数（如 `k` 值、`max_token_limit`）观察效果
- 思考每个示例后的思考题
- 尝试将 Memory 集成到自己的项目中

---

## 🔍 深入理解

### Token 是什么？
- Token 是 LLM 处理文本的基本单位
- 大约 1 个中文字 ≈ 1-2 个 tokens
- 大约 1 个英文单词 ≈ 1-2 个 tokens
- OpenAI 按 token 数量计费

### 为什么需要 Memory？
- LLM 本身是无状态的，不记得之前的对话
- Memory 让 LLM 能够记住对话历史
- 不同的 Memory 类型适合不同的应用场景

### 如何选择 Memory 类型？

```
开始
  ↓
对话轮数多吗？
  ├─ 否（<10轮）→ ConversationBufferMemory
  └─ 是（>10轮）
      ↓
  需要完整的早期历史吗？
      ├─ 否 → ConversationBufferWindowMemory
      └─ 是
          ↓
      有 API 预算吗？
          ├─ 否 → ConversationBufferWindowMemory（k 值设大一点）
          └─ 是 → ConversationSummaryBufferMemory ⭐
```

---

## 🎯 思考题答案

### 02_window_memory.py
1. **k=3 会保存多少条消息？** 
   答：6 条（3 轮 × 2 条/轮 = 6 条）

2. **什么场景下应该使用较小的 k 值？**
   答：token 限制严格、对话内容相对独立、成本敏感

3. **如何选择合适的 k 值？**
   答：考虑任务需要的上下文长度、模型的 token 限制、成本预算

### 03_summary_memory.py
1. **什么场景下应该使用摘要内存？**
   答：超长对话、需要历史概要但不需要完整细节、token 成本高

2. **如果对话每轮都生成摘要，成本会如何？**
   答：成本会很高，因为每次都要调用 LLM。实际上摘要是增量更新的。

3. **如何评估摘要的质量？**
   答：检查关键信息是否保留、是否有幻觉、是否能支持后续对话

### 04_summary_buffer_memory.py
1. **为什么要同时保留摘要和完整消息？**
   答：摘要保留早期关键信息，完整消息提供近期详细上下文

2. **如何确定合适的 max_token_limit 值？**
   答：根据模型上下文长度、成本预算、业务需要的上下文深度

3. **什么情况下这个方案比单纯的窗口内存更好？**
   答：需要早期历史信息时（如客户背景）、对话很长但不想丢失早期关键点

---

## 📖 相关资源

- [LangChain 官方文档](https://python.langchain.com/docs/modules/memory/)
- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
- [Token 计算器](https://platform.openai.com/tokenizer)

---

## 🤝 贡献

如果你有更好的示例或发现了问题，欢迎提出建议！

## 📝 许可

MIT License

---

**祝学习愉快！🎉**
