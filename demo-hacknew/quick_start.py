"""
LangChain 自定义工具快速入门

这是一个最简单的示例，展示如何快速创建和使用自定义工具。
"""

import os
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek

# 设置API密钥
os.environ["DEEPSEEK_API_KEY"] = "sk-915b0213517e462b838b932e5e28b272"

# === 步骤 1: 创建自定义工具 ===

@tool
def add_numbers(a: float, b: float) -> str:
    """将两个数字相加
    
    Args:
        a: 第一个数字
        b: 第二个数字
    
    Returns:
        str: 相加的结果
    """
    result = a + b
    return f"{a} + {b} = {result}"

@tool  
def get_string_length(text: str) -> str:
    """计算字符串的长度
    
    Args:
        text: 要计算长度的字符串
    
    Returns:
        str: 字符串长度信息
    """
    length = len(text)
    return f"字符串 '{text}' 的长度是 {length} 个字符"

# === 步骤 2: 创建工具列表 ===
tools = [add_numbers, get_string_length]

# === 步骤 3: 创建代理 ===
model = ChatDeepSeek(model="deepseek-chat")
agent = create_agent(model, tools=tools)

# === 步骤 4: 使用代理 ===
def main():
    print("=== LangChain 自定义工具快速入门 ===\n")
    
    # 测试用例
    test_queries = [
        "帮我计算 15 + 27 的结果",
        "计算字符串'Hello World'的长度",
        "把 3.14 和 2.86 相加",
        "统计一下'人工智能很有趣'这句话有多少个字符"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"测试 {i}: {query}")
        
        try:
            # 调用代理
            response = agent.invoke({
                "messages": [{"role": "user", "content": query}]
            })
            
            # 输出结果
            print(f"回答: {response['messages'][-1].content}")
            
        except Exception as e:
            print(f"错误: {str(e)}")
        
        print("-" * 50)

if __name__ == "__main__":
    main()








