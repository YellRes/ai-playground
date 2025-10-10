import os
import json
import requests
from typing import Dict, Any, List
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from langchain_community.document_loaders import WebBaseLoader
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

# 设置环境变量（如果需要使用Agent）
# os.environ["DEEPSEEK_API_KEY"] = "your-api-key-here"

os.environ["DEEPSEEK_API_KEY"] = "sk-915b0213517e462b838b932e5e28b272"

@tool
def get_hackernews_top_stories(num_stories: int = 10) -> str:
    """获取 HackerNews 当前的热门文章
    
    Args:
        num_stories: 要获取的热门文章数量，默认为10
    
    Returns:
        str: 格式化的热门文章列表
    """
    try:
        # 获取热门文章ID列表
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_stories_url, timeout=10)
        response.raise_for_status()
        
        story_ids = response.json()[:num_stories]
        
        results = []
        results.append(f"🔥 HackerNews 热门文章 TOP {num_stories}:\n")
        
        # 获取每篇文章的详细信息
        for i, story_id in enumerate(story_ids, 1):
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url, timeout=10)
            
            if story_response.status_code == 200:
                story = story_response.json()
                title = story.get("title", "无标题")
                author = story.get("by", "未知作者")
                score = story.get("score", 0)
                descendants = story.get("descendants", 0)
                url = story.get("url", "")
                
                result_text = f"""
{i}. 📰 {title}
   👤 作者: {author}
   ⬆️  点数: {score} | 💬 评论: {descendants}
   🔗 链接: {url if url else f'https://news.ycombinator.com/item?id={story_id}'}
"""
                results.append(result_text)
        
        return "\n".join(results)
        
    except requests.exceptions.Timeout:
        return "请求超时，请稍后重试"
    except requests.exceptions.RequestException as e:
        return f"API 请求失败: {str(e)}"
    except Exception as e:
        return f"获取热门文章时出现错误: {str(e)}"

@tool
def summarize_url_content(url: str) -> str:
    """总结指定URL网页的内容
    
    这个工具使用 WebBaseLoader 加载网页内容，并使用 AI 模型进行总结。
    适合用于总结 HackerNews 文章链接或其他网页内容。
    
    Args:
        url: 要总结的网页 URL
    
    Returns:
        str: 网页内容的总结
    """
    try:
        # 使用 WebBaseLoader 加载网页内容
        loader = WebBaseLoader(url)
        docs = loader.load()
        
        if not docs:
            return f"无法加载 URL: {url}"
        
        # 获取网页内容
        content = docs[0].page_content
        
        # 如果内容太长，截取前3000个字符
        max_length = 3000
        if len(content) > max_length:
            content = content[:max_length] + "..."
        
        # 使用 AI 模型总结内容
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if api_key:
            model = ChatDeepSeek(model="deepseek-chat")
            prompt = f"""请用中文总结以下网页内容，包括：
1. 主要主题
2. 关键要点（3-5点）
3. 重要结论或观点

网页内容：
{content}

请提供简洁清晰的总结："""
            
            response = model.invoke(prompt)
            summary = response.content
            
            result = f"""
🔍 网页内容总结
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 URL: {url}
📄 内容长度: {len(docs[0].page_content)} 字符

📝 内容总结:
{summary}
"""
            return result
        else:
            # 如果没有 API Key，返回原始内容的前500个字符
            return f"""
🔍 网页内容预览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 URL: {url}
📄 内容长度: {len(content)} 字符

📝 内容预览:
{content[:500]}...

⚠️  提示: 设置 DEEPSEEK_API_KEY 可获取 AI 总结
"""
    
    except Exception as e:
        return f"总结URL内容时出现错误: {str(e)}\n可能原因: 网页无法访问、网络问题或内容加载失败"


# 工具列表
tools = [
    get_hackernews_top_stories,
    summarize_url_content
]

def create_agent_with_memory(model, tools):
    """创建带有记忆功能的 Agent
    
    使用 LangGraph 构建状态图，支持：
    - 多轮对话记忆
    - 工具调用
    - 对话历史保存
    
    Args:
        model: 语言模型实例
        tools: 工具列表
    
    Returns:
        编译后的状态图（带记忆功能）
    """
    
    # 定义 agent 节点：调用模型决定是否使用工具
    def call_model(state: MessagesState):
        """调用模型，可能会返回工具调用"""
        llm_with_tools = model.bind_tools(tools)
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}
    
    # 创建工具节点
    tool_node = ToolNode(tools)
    
    # 构建状态图
    graph_builder = StateGraph(MessagesState)
    
    # 添加节点
    graph_builder.add_node("agent", call_model)
    graph_builder.add_node("tools", tool_node)
    
    # 设置入口点
    graph_builder.set_entry_point("agent")
    
    # 添加条件边：根据是否有工具调用决定下一步
    graph_builder.add_conditional_edges(
        "agent",
        tools_condition,  # 判断是否需要调用工具
        {
            "tools": "tools",  # 如果需要工具，跳转到工具节点
            END: END  # 否则结束
        }
    )
    
    # 工具执行后返回 agent 节点
    graph_builder.add_edge("tools", "agent")
    
    # 添加记忆检查点
    memory = MemorySaver()
    
    # 编译图
    graph = graph_builder.compile(checkpointer=memory)
    
    return graph

def main():
    """主函数：演示如何在 Agent 中使用工具（带记忆功能）"""
    
    # 如果要使用 Agent，需要设置 API Key
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    
    if not api_key:
        print("⚠️  未设置 DEEPSEEK_API_KEY，仅运行工具测试\n")
        return
    
    # 创建模型和带记忆的代理
    model = ChatDeepSeek(model="deepseek-chat")
    agent = create_agent_with_memory(model, tools=tools)
    
    print("=== HackerNews Agent (带记忆功能) ===\n")
    print("💡 提示: 该 Agent 支持多轮对话，会记住之前的对话内容\n")
    
    # 配置：使用 thread_id 来标识对话会话
    config = {"configurable": {"thread_id": "hackernews_session_1"}}
    
    # 测试多轮对话
    test_queries = [
        "给我看看 HackerNews 上现在最热门的5篇文章",
        "帮我总结第一篇文章的内容",  # 这个查询会利用之前对话的上下文
        "第二篇文章是关于什么的？",    # 这个也会利用记忆
    ]
    
    # 执行多轮对话
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"📝 第 {i} 轮对话")
        print(f"{'='*60}")
        print(f"👤 用户: {query}\n")
        
        # 使用相同的 config 来保持对话记忆
        result = agent.invoke(
            {"messages": [{"role": "user", "content": query}]},
            config=config
        )
        
        # 获取最后一条 AI 消息
        last_message = result['messages'][-1]
        print(f"🤖 AI 回答:\n{last_message.content}\n")

def main_interactive():
    """交互式对话模式：支持持续对话"""
    
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    
    if not api_key:
        print("⚠️  未设置 DEEPSEEK_API_KEY\n")
        return
    
    # 创建模型和带记忆的代理
    model = ChatDeepSeek(model="deepseek-chat")
    agent = create_agent_with_memory(model, tools=tools)
    
    print("=== HackerNews Agent 交互式对话 ===\n")
    print("💡 提示:")
    print("  - 该 Agent 会记住所有对话历史")
    print("  - 输入 'exit' 或 'quit' 退出")
    print("  - 输入 'clear' 清除对话历史\n")
    print(f"{'='*60}\n")
    
    # 对话会话 ID
    thread_id = "interactive_session"
    config = {"configurable": {"thread_id": thread_id}}
    
    conversation_count = 0
    
    while True:
        try:
            # 获取用户输入
            user_input = input("👤 您: ").strip()
            
            if not user_input:
                continue
            
            # 退出命令
            if user_input.lower() in ['exit', 'quit', '退出']:
                print("\n👋 再见！")
                break
            
            # 清除历史命令
            if user_input.lower() in ['clear', '清除']:
                conversation_count = 0
                thread_id = f"interactive_session_{os.urandom(4).hex()}"
                config = {"configurable": {"thread_id": thread_id}}
                print("\n✨ 对话历史已清除\n")
                continue
            
            conversation_count += 1
            
            # 调用 agent
            result = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config=config
            )
            
            # 显示回复
            last_message = result['messages'][-1]
            print(f"\n🤖 AI: {last_message.content}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}\n")


if __name__ == "__main__":
    import sys
    
    # 根据命令行参数选择运行模式
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        # 交互式对话模式
        main_interactive()
    else:
        # 默认：运行多轮对话测试
        main()
    
    # 提示：如何运行交互式模式
    if len(sys.argv) == 1:
        print("\n" + "="*60)
        print("💡 提示: 运行 'python index.py interactive' 进入交互式对话模式")
        print("="*60)