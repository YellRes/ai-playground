"""
LangChain Memory 示例 1: ConversationBufferMemory
==============================================
这是最基础的内存类型，会完整保存所有对话历史
适用场景：对话轮数较少，需要保留完整上下文
"""

from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain

def demo_basic_buffer():
    """演示最基础的 Buffer Memory 用法"""
    print("=" * 50)
    print("演示 1: 基础用法 - 手动添加消息")
    print("=" * 50)
    
    # 初始化内存
    memory = ConversationBufferMemory()
    
    # 手动添加对话消息
    memory.chat_memory.add_user_message("你好！我叫小明")
    memory.chat_memory.add_ai_message("你好小明！很高兴认识你！")
    memory.chat_memory.add_user_message("今天天气真好")
    memory.chat_memory.add_ai_message("是的，阳光明媚的日子让人心情愉悦！")
    
    # 查看保存的内容
    print("\n💾 当前内存中的对话历史：")
    print(memory.load_memory_variables({}))
    
    print("\n✨ 观察：所有对话都被完整保存了！")


def demo_with_chain():
    """演示在对话链中使用 Buffer Memory"""
    print("\n" + "=" * 50)
    print("演示 2: 在对话链中使用")
    print("=" * 50)
    
    # 初始化 LLM 和 Memory
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    memory = ConversationBufferMemory()
    
    # 创建对话链
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True  # 显示详细信息
    )
    
    print("\n🤖 开始多轮对话：")
    
    # 第一轮对话
    print("\n👤 用户: 我最喜欢的颜色是蓝色")
    response1 = conversation.predict(input="我最喜欢的颜色是蓝色")
    print(f"🤖 AI: {response1}")
    
    # 第二轮对话 - AI 应该记得之前说的颜色
    print("\n👤 用户: 你还记得我喜欢什么颜色吗？")
    response2 = conversation.predict(input="你还记得我喜欢什么颜色吗？")
    print(f"🤖 AI: {response2}")
    
    # 查看内存内容
    print("\n💾 最终内存状态：")
    print(memory.load_memory_variables({}))


def demo_save_context():
    """演示使用 save_context 方法"""
    print("\n" + "=" * 50)
    print("演示 3: 使用 save_context 方法")
    print("=" * 50)
    
    memory = ConversationBufferMemory()
    
    # 使用 save_context 批量保存对话
    conversations = [
        ({"input": "什么是 Python？"}, {"output": "Python 是一种高级编程语言"}),
        ({"input": "它的优点是什么？"}, {"output": "Python 语法简洁，易于学习"}),
        ({"input": "谢谢！"}, {"output": "不客气！"}),
    ]
    
    for user_msg, ai_msg in conversations:
        memory.save_context(user_msg, ai_msg)
        print(f"👤 {user_msg['input']}")
        print(f"🤖 {ai_msg['output']}\n")
    
    # 查看保存的历史
    print("💾 完整对话历史：")
    history = memory.load_memory_variables({})
    print(history)


if __name__ == "__main__":
    print("🎓 LangChain Memory 教程 - ConversationBufferMemory\n")
    
    # 运行演示 1
    demo_basic_buffer()
    
    # 运行演示 3（不需要 API key）
    demo_save_context()
    
    # 运行演示 2（需要 OpenAI API key）
    print("\n" + "=" * 50)
    print("⚠️  演示 2 需要 OpenAI API Key")
    print("如果您已配置，请取消下面的注释：")
    print("=" * 50)
    # demo_with_chain()
    
    print("\n" + "=" * 50)
    print("📚 知识点总结")
    print("=" * 50)
    print("""
    ConversationBufferMemory 特点：
    ✅ 保存完整的对话历史
    ✅ 实现简单，易于理解
    ❌ 随着对话增长，内存占用会持续增加
    ❌ 超长对话可能超出 LLM 的 token 限制
    
    适用场景：
    - 短对话场景
    - 需要完整上下文的应用
    - 开发和测试阶段
    """)

