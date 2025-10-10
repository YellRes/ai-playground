import os
import json
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from getBalanceSheet import get_balance_sheet
from pydantic import BaseModel

os.environ["DEEPSEEK_API_KEY"] = "sk-915b0213517e462b838b932e5e28b272"

class Answer(BaseModel):
    content: str

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search for information."""
    # 找到公司的信息
    with open("szse_stock.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # 在数据中搜索zwjc字段等于query的项目
    stocks = data.get("stockList") or []
    found_items = []

    for item in stocks:
        if item.get("zwjc") == query:
            found_items.append(item)
            break
    
    print(f"搜索'{query}'的结果:", found_items)
    
    if not found_items:
        return f"未找到与'{query}'匹配的公司"
    
    code = found_items[0].get('code', '')
    return f"code: {code}, zwjc: {found_items[0].get('zwjc', '')}"


@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    print("调用了 multiply")
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Add a and b.

    Args:
        a: first int
        b: second int
    """
    print("调用了 add")
    return a + b



model = ChatDeepSeek(model="deepseek-chat")
agent = create_agent(model, tools=[multiply, add], response_format=Answer)

# agent = create_agent(model, tools=[search_database, multiply], response_format=Company)


# res = agent.invoke({"messages": [{"role": "user", "content": "你好"}]})
# res = agent.invoke({"messages": [{"role": "user", "content": "2 乘上 3"}]})
res = agent.invoke({"messages": [{"role": "user", "content": "2 加上 3 乘上 3 "}]})


print(res["structured_response"])
