"""
LangChain 自定义工具的完整演示

这个文件展示了如何创建和使用各种类型的自定义工具，
包括简单工具、复杂工具、错误处理等。
"""

import os
from langchain_core.tools import tool, StructuredTool
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel, Field
from typing import Type, Any

# 设置环境变量
os.environ["DEEPSEEK_API_KEY"] = "sk-915b0213517e462b838b932e5e28b272"

# === 方法 1: 基本的 @tool 装饰器 ===
@tool
def simple_calculator(expression: str) -> str:
    """执行简单的数学计算
    
    Args:
        expression: 数学表达式，如 "2+3*4"
    
    Returns:
        str: 计算结果
    """
    try:
        # 为了安全，只允许基本的数学运算
        allowed_chars = set('0123456789+-*/().')
        if not all(c in allowed_chars or c.isspace() for c in expression):
            return "错误：表达式包含不允许的字符"
        
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"

# === 方法 2: 使用 Pydantic 模型定义工具输入 ===
class TextAnalysisInput(BaseModel):
    """文本分析工具的输入模型"""
    text: str = Field(description="要分析的文本内容")
    analysis_type: str = Field(
        description="分析类型：length（长度）, words（词数）, sentiment（情感）",
        default="length"
    )

@tool(args_schema=TextAnalysisInput)
def advanced_text_analyzer(text: str, analysis_type: str = "length") -> str:
    """高级文本分析工具
    
    支持多种分析类型的文本分析
    """
    if not text.strip():
        return "错误：文本内容为空"
    
    if analysis_type == "length":
        return f"文本长度：{len(text)} 个字符"
    elif analysis_type == "words":
        words = text.split()
        return f"词数统计：{len(words)} 个词"
    elif analysis_type == "sentiment":
        # 简单的情感分析
        positive_words = ['好', '棒', '优秀', '满意', '开心', '喜欢']
        negative_words = ['坏', '差', '失败', '不满', '难过', '讨厌']
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count > negative_count:
            sentiment = "正面"
        elif negative_count > positive_count:
            sentiment = "负面"
        else:
            sentiment = "中性"
        
        return f"情感分析：{sentiment}（正面词:{positive_count}, 负面词:{negative_count}）"
    else:
        return f"错误：不支持的分析类型 '{analysis_type}'"

# === 方法 3: 使用 StructuredTool 类创建工具 ===
def get_user_info(user_id: str) -> str:
    """获取用户信息的函数"""
    # 模拟用户数据库
    users = {
        "001": {"name": "张三", "age": 25, "city": "北京"},
        "002": {"name": "李四", "age": 30, "city": "上海"},
        "003": {"name": "王五", "age": 28, "city": "深圳"}
    }
    
    if user_id in users:
        user = users[user_id]
        return f"用户 {user_id}: 姓名={user['name']}, 年龄={user['age']}, 城市={user['city']}"
    else:
        return f"未找到用户 ID: {user_id}"

# 使用 StructuredTool.from_function 创建工具
user_info_tool = StructuredTool.from_function(
    func=get_user_info,
    name="get_user_info",
    description="根据用户ID获取用户详细信息"
)

# === 方法 4: 带错误处理的工具 ===
@tool
def safe_file_reader(filename: str) -> str:
    """安全的文件读取工具
    
    Args:
        filename: 要读取的文件名
    
    Returns:
        str: 文件内容或错误信息
    """
    try:
        # 安全检查：只允许读取当前目录下的 txt 文件
        if not filename.endswith('.txt'):
            return "错误：只能读取 .txt 文件"
        
        if '/' in filename or '\\' in filename:
            return "错误：文件名不能包含路径分隔符"
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if len(content) > 1000:
            return f"文件内容（前1000字符）：\n{content[:1000]}...\n\n文件总长度：{len(content)} 字符"
        else:
            return f"文件内容：\n{content}"
            
    except FileNotFoundError:
        return f"错误：文件 '{filename}' 不存在"
    except PermissionError:
        return f"错误：没有权限读取文件 '{filename}'"
    except Exception as e:
        return f"读取文件时发生未知错误：{str(e)}"

# === 方法 5: 异步工具（如果需要的话）===
@tool
def mock_api_call(api_name: str, params: str = "") -> str:
    """模拟 API 调用
    
    Args:
        api_name: API 名称
        params: API 参数（可选）
    
    Returns:
        str: API 响应
    """
    import time
    import random
    
    # 模拟网络延迟
    time.sleep(random.uniform(0.1, 0.5))
    
    # 模拟不同的 API 响应
    if api_name == "weather":
        return f"天气API响应：今日天气晴朗，温度 22°C（参数：{params}）"
    elif api_name == "news":
        return f"新闻API响应：今日热门新闻3条（参数：{params}）"
    elif api_name == "stock":
        price = random.uniform(10, 100)
        return f"股票API响应：当前价格 ¥{price:.2f}（参数：{params}）"
    else:
        return f"错误：未知的API '{api_name}'"

# === 创建工具列表 ===
all_tools = [
    simple_calculator,
    advanced_text_analyzer,
    user_info_tool,
    safe_file_reader,
    mock_api_call
]

def demonstrate_tools():
    """演示各种自定义工具的使用"""
    
    print("=== LangChain 自定义工具完整演示 ===\n")
    
    # 创建模型和代理
    model = ChatDeepSeek(model="deepseek-chat")
    agent = create_agent(model, tools=all_tools)
    
    # 测试用例
    test_cases = [
        {
            "description": "基本计算器测试",
            "query": "计算 (10 + 5) * 3 - 8 的结果"
        },
        {
            "description": "文本长度分析",
            "query": "分析这段文本的长度：人工智能是未来科技发展的重要方向"
        },
        {
            "description": "情感分析",
            "query": "分析这段文本的情感：今天工作很顺利，我很开心很满意"
        },
        {
            "description": "用户信息查询",
            "query": "查询用户ID为002的详细信息"
        },
        {
            "description": "模拟API调用",
            "query": "调用天气API，参数为北京"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🧪 测试 {i}: {test_case['description']}")
        print(f"📝 问题: {test_case['query']}")
        
        try:
            result = agent.invoke({
                "messages": [{"role": "user", "content": test_case['query']}]
            })
            print(f"🤖 回答: {result['messages'][-1].content}")
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
        
        print("-" * 60)

def show_tool_info():
    """显示所有工具的信息"""
    print("=== 可用工具列表 ===\n")
    
    for i, tool in enumerate(all_tools, 1):
        print(f"{i}. 工具名称: {tool.name}")
        print(f"   描述: {tool.description}")
        print(f"   参数: {tool.args}")
        print()

if __name__ == "__main__":
    # 显示工具信息
    show_tool_info()
    
    # 演示工具使用
    demonstrate_tools()
    
    print("\n=== 交互式测试 ===")
    print("你可以直接向代理提问，它会自动选择合适的工具来回答。")
    print("输入 'quit' 退出程序。\n")
    
    # 创建交互式代理
    model = ChatDeepSeek(model="deepseek-chat")
    agent = create_agent(model, tools=all_tools)
    
    while True:
        try:
            user_input = input("🧑 你的问题: ").strip()
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("👋 再见！")
                break
                
            if not user_input:
                continue
                
            result = agent.invoke({
                "messages": [{"role": "user", "content": user_input}]
            })
            print(f"🤖 助手: {result['messages'][-1].content}\n")
            
        except KeyboardInterrupt:
            print("\n👋 程序已退出！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {str(e)}\n")








