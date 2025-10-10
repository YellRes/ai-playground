from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
import os

os.environ["DEEPSEEK_API_KEY"] = "sk-915b0213517e462b838b932e5e28b272"
model = init_chat_model(model="deepseek")

system_message = SystemMessage("You are a helpful assistant.")
human_message = HumanMessage("hello, how are you?")

messages = [system_message, human_message]
response = model.invoke(messages)