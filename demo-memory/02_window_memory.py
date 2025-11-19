"""
LangChain Memory 示例 2: ConversationBufferWindowMemory
=======================================================
窗口内存：只保留最近的 K 轮对话
适用场景：长对话场景，控制内存大小，避免超出 token 限制
"""

from langchain.memory import ConversationBufferWindowMemory

def demo_window_memory():
    """演示窗口内存的基本用法"""
    print("=" * 50)
    print("演示 1: 窗口大小 k=2")
    print("=" * 50)
    
    # 创建窗口内存，只保留最近 2 轮对话
    memory = ConversationBufferWindowMemory(k=2)
    
    # 模拟多轮对话
    conversations = [
        ("你好，我是小明", "你好小明！"),
        ("我今年 18 岁", "知道了，你 18 岁。"),
        ("我喜欢编程", "编程是个很好的爱好！"),
        ("我最喜欢 Python", "Python 确实很棒！"),
    ]
    
    for i, (user_msg, ai_msg) in enumerate(conversations, 1):
        memory.save_context(
            {"input": user_msg},
            {"output": ai_msg}
        )
        print(f"\n📍 第 {i} 轮对话后：")
        print(f"👤 用户: {user_msg}")
        print(f"🤖 AI: {ai_msg}")
        
        # 显示当前内存内容
        history = memory.load_memory_variables({})
        print(f"\n💾 当前内存中的对话（最多保留 {memory.k} 轮）：")
        print(history['history'])
        print("-" * 50)


def demo_different_window_sizes():
    """对比不同窗口大小的效果"""
    print("\n" + "=" * 50)
    print("演示 2: 对比不同窗口大小")
    print("=" * 50)
    
    # 准备相同的对话数据
    conversations = [
        ("第1句", "回复1"),
        ("第2句", "回复2"),
        ("第3句", "回复3"),
        ("第4句", "回复4"),
        ("第5句", "回复5"),
    ]
    
    # 测试不同的窗口大小
    for k in [1, 2, 3]:
        print(f"\n🔍 窗口大小 k={k}:")
        memory = ConversationBufferWindowMemory(k=k)
        
        # 添加所有对话
        for user_msg, ai_msg in conversations:
            memory.save_context(
                {"input": user_msg},
                {"output": ai_msg}
            )
        
        # 显示保留的内容
        history = memory.load_memory_variables({})
        print(f"保留的内容: {history['history']}")


def demo_return_messages():
    """演示返回消息对象而非字符串"""
    print("\n" + "=" * 50)
    print("演示 3: 返回消息对象")
    print("=" * 50)
    
    # return_messages=True 会返回消息对象列表
    memory = ConversationBufferWindowMemory(
        k=2,
        return_messages=True
    )
    
    # 添加对话
    memory.save_context(
        {"input": "你好"},
        {"output": "你好！有什么可以帮助你的？"}
    )
    memory.save_context(
        {"input": "介绍一下 Python"},
        {"output": "Python 是一种解释型、面向对象的编程语言"}
    )
    
    # 获取消息列表
    history = memory.load_memory_variables({})
    print("\n💾 返回的消息对象：")
    for msg in history['history']:
        print(f"类型: {type(msg).__name__}")
        print(f"内容: {msg.content}")
        print(f"角色: {msg.__class__.__name__}")
        print("-" * 30)


def demo_practical_example():
    """实际应用示例：客服对话"""
    print("\n" + "=" * 50)
    print("演示 4: 实际应用 - 客服对话场景")
    print("=" * 50)
    
    # 客服场景：只需要记住最近3轮对话
    memory = ConversationBufferWindowMemory(k=3)
    
    print("\n📞 客服对话开始：\n")
    
    dialogs = [
        ("你们的营业时间是？", "我们的营业时间是周一到周五 9:00-18:00"),
        ("周末营业吗？", "抱歉，周末我们不营业"),
        ("你们在哪里？", "我们位于北京市朝阳区"),
        ("能送货吗？", "可以，我们提供配送服务"),
        ("配送费多少？", "市内配送免费，郊区收费20元"),
        # 这时候第1、2轮对话应该被遗忘了
        ("你们营业时间是？", "（AI应该不记得之前问过这个问题）"),
    ]
    
    for i, (question, answer) in enumerate(dialogs, 1):
        memory.save_context(
            {"input": question},
            {"output": answer}
        )
        
        print(f"第 {i} 轮:")
        print(f"  👤 客户: {question}")
        print(f"  🤖 客服: {answer}")
        
        # 每轮后显示记忆内容
        if i % 2 == 0:  # 每2轮显示一次
            history = memory.load_memory_variables({})
            print(f"\n  💾 当前记忆的对话轮数: {len(memory.chat_memory.messages) // 2}")
            print()


if __name__ == "__main__":
    print("🎓 LangChain Memory 教程 - ConversationBufferWindowMemory\n")
    
    # 运行所有演示
    demo_window_memory()
    demo_different_window_sizes()
    demo_return_messages()
    demo_practical_example()
    
    print("\n" + "=" * 50)
    print("📚 知识点总结")
    print("=" * 50)
    print("""
    ConversationBufferWindowMemory 特点：
    ✅ 控制内存大小，避免无限增长
    ✅ 保证不会超出 token 限制
    ✅ 适合长对话场景
    ❌ 会丢失较早的对话历史
    ❌ 可能丢失重要的上下文信息
    
    关键参数：
    - k: 保留最近的 k 轮对话
    - return_messages: True 返回消息对象，False 返回字符串
    
    适用场景：
    - 长对话/多轮对话
    - 只需要短期上下文的应用
    - 客服、问答等场景
    
    💡 思考题：
    1. 如果 k=3，那么会保存多少条消息？（提示：一轮=用户+AI）
    2. 什么场景下应该使用较小的 k 值？
    3. 如何选择合适的 k 值？
    """)

