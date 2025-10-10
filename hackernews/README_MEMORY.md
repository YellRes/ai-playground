# HackerNews Agent 记忆系统使用指南

## 🎯 功能概述

现在 HackerNews Agent 支持**对话记忆功能**，能够记住之前的对话内容，实现智能的多轮对话！

## 🔧 核心改动

### 1. 新增依赖
```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
```

### 2. 创建带记忆的 Agent
新增了 `create_agent_with_memory()` 函数，使用 LangGraph 构建状态图：

```python
def create_agent_with_memory(model, tools):
    """创建带有记忆功能的 Agent"""
    # ... 构建状态图
    memory = MemorySaver()  # 记忆保存器
    graph = graph_builder.compile(checkpointer=memory)
    return graph
```

### 3. 工作流程

```
用户输入
    ↓
┌──────────┐
│  agent   │ ← 调用 LLM 决定是否使用工具
└────┬─────┘
     │
[条件判断]
    ↙    ↘
需要工具   直接回答
   ↓       ↓
┌──────┐  END
│tools │
└──┬───┘
   ↓
返回 agent (处理工具结果)
```

## 🚀 使用方法

### 方式一：多轮对话测试（默认）

```bash
python index.py
```

这会运行预设的多轮对话测试，演示记忆功能：
1. 获取热门文章
2. 总结第一篇（利用第一步的上下文）
3. 询问第二篇（继续利用记忆）

### 方式二：交互式对话模式

```bash
python index.py interactive
```

进入交互式对话，可以：
- 持续与 Agent 对话，它会记住所有历史
- 输入 `exit` 或 `quit` 退出
- 输入 `clear` 清除对话历史

## 💡 关键概念

### Thread ID（会话 ID）
```python
config = {"configurable": {"thread_id": "conversation_1"}}
```

- 用于标识不同的对话会话
- 相同 `thread_id` 的调用共享对话记忆
- 不同 `thread_id` 的对话相互独立

### MessagesState
- 自动管理消息历史
- 每次调用会自动追加新消息
- 支持多种消息类型：human, ai, tool, system

## 📝 示例对话

```python
# 第一轮
用户: "给我看看 HackerNews 最热门的5篇文章"
AI: [调用工具获取文章列表]

# 第二轮 - 利用记忆
用户: "总结第一篇的内容"
AI: [知道第一篇是什么，调用总结工具]

# 第三轮 - 继续利用记忆
用户: "第二篇呢？"
AI: [知道指的是文章列表中的第二篇]
```

## 🔍 记忆系统的优势

1. **上下文理解**：Agent 能理解"第一篇"、"它"等代词指代
2. **连续对话**：不需要重复提供背景信息
3. **智能推理**：基于历史对话做出更好的决策
4. **会话管理**：可以管理多个独立的对话会话

## 🛠️ 技术细节

### MemorySaver
- 在内存中保存对话状态
- 支持检查点（checkpoint）机制
- 可以序列化/反序列化状态

### 状态图节点
- **agent 节点**：调用 LLM，决定是否使用工具
- **tools 节点**：执行工具调用
- **循环机制**：工具执行后返回 agent 处理结果

### 条件边 (tools_condition)
自动判断：
- 如果 AI 返回包含 `tool_calls` → 跳转到 tools 节点
- 如果 AI 直接回答 → 结束流程

## 📦 依赖安装

如果遇到导入错误，请安装：
```bash
pip install langgraph
pip install langchain-core
```

## 🎮 实战建议

1. **明确会话边界**：为不同用户或任务使用不同的 `thread_id`
2. **定期清理历史**：长对话可能影响性能，适时清除
3. **测试边界情况**：测试 Agent 如何处理模糊的代词引用
4. **监控 token 使用**：记忆会增加上下文长度

## 🔗 相关资源

- [LangGraph 文档](https://python.langchain.com/docs/langgraph)
- [MemorySaver API](https://python.langchain.com/docs/langgraph/reference/checkpointers)
- [MessagesState](https://python.langchain.com/docs/langgraph/reference/graphs)
