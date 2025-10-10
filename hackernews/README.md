# HackerNews LangChain 工具集

这是一个完整的 HackerNews API LangChain 工具集，提供了搜索、获取热门文章和文章详情等功能。

## 功能特性

### 🔍 1. search_hackernews - 搜索工具
搜索 HackerNews 上的文章和讨论

**参数：**
- `query` (str): 搜索关键词
- `num_results` (int): 返回结果数量，默认为 10

**示例：**
```python
result = search_hackernews.invoke({"query": "Python", "num_results": 5})
```

### 🔥 2. get_hackernews_top_stories - 热门文章
获取 HackerNews 当前的热门文章

**参数：**
- `num_stories` (int): 要获取的文章数量，默认为 10

**示例：**
```python
result = get_hackernews_top_stories.invoke({"num_stories": 5})
```

### 📰 3. get_hackernews_story_details - 文章详情
获取指定 HackerNews 文章的详细信息

**参数：**
- `story_id` (str): HackerNews 文章的 ID

**示例：**
```python
result = get_hackernews_story_details.invoke({"story_id": "12345678"})
```

## 使用方法

### 方法1：直接使用工具（无需 Agent）

```python
from index import search_hackernews, get_hackernews_top_stories

# 搜索文章
result = search_hackernews.invoke({"query": "AI", "num_results": 5})
print(result)

# 获取热门文章
result = get_hackernews_top_stories.invoke({"num_stories": 5})
print(result)
```

### 方法2：使用 LangChain Agent

```python
import os
from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent
from index import tools

# 设置 API Key
os.environ["DEEPSEEK_API_KEY"] = "your-api-key"

# 创建模型和代理
model = ChatDeepSeek(model="deepseek-chat")
agent = create_agent(model, tools=tools)

# 使用自然语言查询
result = agent.invoke({
    "messages": [{"role": "user", "content": "搜索关于 Python 的文章"}]
})
print(result['messages'][-1].content)
```

### 方法3：运行测试

```python
# 直接运行文件进行测试
python index.py
```

## API 说明

本工具集使用了两个 HackerNews API：

1. **Algolia HackerNews API** (用于搜索)
   - 端点：`https://hn.algolia.com/api/v1/search`
   - 文档：https://hn.algolia.com/api

2. **Official HackerNews Firebase API** (用于获取热门和详情)
   - 端点：`https://hacker-news.firebaseio.com/v0/`
   - 文档：https://github.com/HackerNews/API

## 依赖项

```bash
pip install langchain langchain-core langchain-deepseek requests
```

## 返回格式示例

### 搜索结果
```
🔍 HackerNews 搜索结果 - 关键词: 'Python'
找到 10 条结果:

1. 📰 Python 3.12 Released
   👤 作者: guido
   ⬆️  点数: 1234 | 💬 评论: 567
   🕒 发布时间: 2025-01-01
   🔗 原文链接: https://www.python.org
   💭 讨论链接: https://news.ycombinator.com/item?id=12345678
```

### 热门文章
```
🔥 HackerNews 热门文章 TOP 5:

1. 📰 Show HN: I built a new tool
   👤 作者: developer
   ⬆️  点数: 890 | 💬 评论: 123
   🔗 链接: https://example.com
```

### 文章详情
```
📰 文章详情 (ID: 12345678)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 标题: Amazing New Technology
👤 作者: techguru
⬆️  点数: 500
💬 评论数: 89
🕒 发布时间: 2025-01-01 10:30:00
🔗 原文链接: https://example.com
💭 讨论链接: https://news.ycombinator.com/item?id=12345678

📝 内容摘要:
This is an amazing article about...
```

## 注意事项

1. **网络请求超时**：所有 API 请求设置了 10 秒超时
2. **错误处理**：所有函数都包含完善的异常处理
3. **速率限制**：注意 HackerNews API 的速率限制，避免频繁请求
4. **API Key**：使用 Agent 时需要设置 DeepSeek API Key

## 扩展功能

你可以基于此工具集添加更多功能：

- 按时间范围过滤搜索结果
- 按分数排序
- 获取评论内容
- 搜索特定作者的文章
- 按标签分类（Ask HN, Show HN 等）

## 许可

本项目使用 MIT 许可证。

