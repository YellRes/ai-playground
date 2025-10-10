from typing_extensions import TypedDict
import os
import json
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel
import random
from typing import Literal
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

os.environ["DEEPSEEK_API_KEY"] = "sk-915b0213517e462b838b932e5e28b272"

class State(TypedDict):
    graph_state: str


def node_1(state):
    print("---Node 1---")
    return {"graph_state": state['graph_state'] +" 我的心情是"}

def node_2(state):
    print("---Node 2---")
    return {"graph_state": state['graph_state'] +" 开心!"}

def node_3(state):
    print("---Node 3---")
    return {"graph_state": state['graph_state'] +" 伤心!"}

def decide_mood(state) -> Literal["node_2", "node_3"]:
    # 通常，我们会使用 state 来决定下一个要访问的节点
    user_input = state['graph_state'] 
    
    # 这里，我们只是做一个在 nodes 2, 3 之间做 50% 的随机选择
    if random.random() < 0.5:

        # 50% 的几率，我们返回 Node 2
        return "node_2"
    
    # 50% 的几率，我们返回 Node 3
    return "node_3"

# Build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Add
graph = builder.compile()

# 方法1: 直接获取最终状态
result = graph.invoke({"graph_state" : "你好，"})
print("\n=== 最终状态 ===")
print(result)

print("\n" + "="*50 + "\n")

# 方法2: 流式输出，查看每个节点的状态变化
# print("=== 流式输出每个节点的状态 ===")
# for step in graph.stream({"graph_state": "Hi, this is Lance."}):
#     print(f"\n当前节点: {list(step.keys())[0]}")
#     print(f"状态内容: {step}")
