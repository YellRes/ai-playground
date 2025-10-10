import os
import json
import datetime
import requests
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel, Field

# 设置环境变量
os.environ["DEEPSEEK_API_KEY"] = "sk-915b0213517e462b838b932e5e28b272"

# 定义数据模型
class Company(BaseModel):
    code: str = Field(description="公司代码")
    zwjc: str = Field(description="公司中文简称")

class WeatherInfo(BaseModel):
    location: str = Field(description="位置")
    temperature: str = Field(description="温度")
    description: str = Field(description="天气描述")

# 方法 1: 使用 @tool 装饰器创建简单工具
@tool
def search_company_database(query: str, limit: int = 10) -> str:
    """在公司数据库中搜索信息
    
    Args:
        query: 要搜索的公司名称
        limit: 返回结果的最大数量
    
    Returns:
        str: 搜索结果，包含公司代码和名称
    """
    try:
        # 模拟从数据库文件中读取数据
        with open("szse_stock.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        stocks = data.get("stockList", [])
        found_items = []

        for item in stocks:
            if query in item.get("zwjc", ""):
                found_items.append(item)
                if len(found_items) >= limit:
                    break
        
        if not found_items:
            return f"未找到与'{query}'匹配的公司"
        
        # 格式化返回结果
        results = []
        for item in found_items:
            code = item.get('code', '')
            name = item.get('zwjc', '')
            results.append(f"代码: {code}, 名称: {name}")
        
        return "\n".join(results)
        
    except FileNotFoundError:
        return f"数据库文件不存在，无法搜索'{query}'"
    except Exception as e:
        return f"搜索过程中出现错误: {str(e)}"

# 方法 2: 带类型提示和复杂参数的工具
@tool
def get_current_time(timezone: str = "Asia/Shanghai") -> str:
    """获取当前时间
    
    Args:
        timezone: 时区，默认为亚洲/上海
    
    Returns:
        str: 格式化的当前时间
    """
    try:
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        return f"当前时间 ({timezone}): {formatted_time}"
    except Exception as e:
        return f"获取时间失败: {str(e)}"

# 方法 3: 模拟外部 API 调用的工具
@tool
def get_weather_info(city: str) -> str:
    """获取指定城市的天气信息
    
    Args:
        city: 城市名称
    
    Returns:
        str: 天气信息
    """
    # 模拟天气数据（实际应用中会调用真实的天气API）
    weather_data = {
        "北京": {"temperature": "15°C", "description": "晴朗"},
        "上海": {"temperature": "18°C", "description": "多云"},
        "深圳": {"temperature": "25°C", "description": "小雨"},
        "广州": {"temperature": "23°C", "description": "阴天"}
    }
    
    if city in weather_data:
        info = weather_data[city]
        return f"{city}的天气: 温度 {info['temperature']}, {info['description']}"
    else:
        return f"暂无{city}的天气信息"

# 方法 4: 处理列表输入的工具
@tool
def calculate_statistics(numbers: str) -> str:
    """计算数字列表的统计信息
    
    Args:
        numbers: 逗号分隔的数字字符串，例如 "1,2,3,4,5"
    
    Returns:
        str: 包含平均值、最大值、最小值的统计信息
    """
    try:
        # 解析数字字符串
        num_list = [float(x.strip()) for x in numbers.split(",")]
        
        if not num_list:
            return "未提供有效的数字"
        
        # 计算统计信息
        avg = sum(num_list) / len(num_list)
        max_val = max(num_list)
        min_val = min(num_list)
        count = len(num_list)
        
        return f"统计结果:\n数量: {count}\n平均值: {avg:.2f}\n最大值: {max_val}\n最小值: {min_val}"
        
    except ValueError:
        return "输入格式错误，请提供逗号分隔的数字"
    except Exception as e:
        return f"计算过程中出现错误: {str(e)}"

# 方法 5: 文件操作工具
@tool
def save_text_to_file(filename: str, content: str) -> str:
    """将文本内容保存到文件
    
    Args:
        filename: 文件名
        content: 要保存的内容
    
    Returns:
        str: 操作结果
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"内容已成功保存到 {filename}"
    except Exception as e:
        return f"保存文件失败: {str(e)}"

# 方法 6: 复杂数据处理工具
@tool
def analyze_text(text: str) -> str:
    """分析文本的基本统计信息
    
    Args:
        text: 要分析的文本
    
    Returns:
        str: 文本分析结果
    """
    if not text:
        return "未提供文本内容"
    
    # 计算基本统计信息
    char_count = len(text)
    word_count = len(text.split())
    line_count = len(text.split('\n'))
    
    # 简单的情感分析（基于关键词）
    positive_words = ['好', '棒', '优秀', '满意', '开心', '喜欢', '成功']
    negative_words = ['坏', '差', '失败', '不满', '难过', '讨厌', '问题']
    
    positive_count = sum(1 for word in positive_words if word in text)
    negative_count = sum(1 for word in negative_words if word in text)
    
    if positive_count > negative_count:
        sentiment = "正面"
    elif negative_count > positive_count:
        sentiment = "负面"
    else:
        sentiment = "中性"
    
    return f"""文本分析结果:
字符数: {char_count}
词数: {word_count}
行数: {line_count}
情感倾向: {sentiment} (正面词:{positive_count}, 负面词:{negative_count})"""

# 工具列表
tools = [
    search_company_database,
    get_current_time,
    get_weather_info,
    calculate_statistics,
    save_text_to_file,
    analyze_text
]

def main():
    """主函数：演示如何使用自定义工具"""
    
    # 创建模型和代理
    model = ChatDeepSeek(model="deepseek-chat")
    agent = create_agent(model, tools=tools)
    
    # 测试不同的工具调用
    test_queries = [
        "帮我搜索金发科技这家公司",
        "现在几点了？",
        "查询一下北京的天气",
        "计算这些数字的统计信息: 10,20,30,40,50",
        "分析这段文本的情感：今天天气真好，我很开心！工作很顺利。"
    ]
    
    print("=== LangChain 自定义工具演示 ===\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"测试 {i}: {query}")
        try:
            result = agent.invoke({"messages": [{"role": "user", "content": query}]})
            print(f"回答: {result['messages'][-1].content}\n")
        except Exception as e:
            print(f"错误: {str(e)}\n")

if __name__ == "__main__":
    main()


