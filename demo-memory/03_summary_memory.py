"""
LangChain Memory 示例 3: ConversationSummaryMemory
==================================================
摘要内存：使用 LLM 生成对话摘要，而非保存完整历史
适用场景：超长对话，需要保留关键信息但控制 token 数量
"""

from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

def demo_summary_memory_basic():
    """演示摘要内存的基本用法"""
    print("=" * 50)
    print("演示 1: 基础摘要生成")
    print("=" * 50)
    print("\n⚠️  此演示需要 OpenAI API Key\n")
    
    # 初始化 LLM（用于生成摘要）
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0  # 温度设为0，让摘要更稳定
    )
    
    # 创建摘要内存
    memory = ConversationSummaryMemory(llm=llm)
    
    # 模拟一段较长的对话
    print("📝 添加对话历史：\n")
    conversations = [
        (
            "你好，我想学习 Python 编程",
            "你好！很高兴能帮助你学习 Python。Python 是一种非常适合初学者的编程语言，语法简洁易懂。你之前有编程经验吗？"
        ),
        (
            "没有，我是完全的新手",
            "没关系！作为新手，我建议你从基础语法开始，比如变量、数据类型、条件语句和循环。我可以为你推荐一些学习资源。"
        ),
        (
            "那我应该用什么工具来写代码？",
            "对于初学者，我推荐使用 VS Code 或 PyCharm。VS Code 轻量级且免费，PyCharm 功能更强大但稍重。另外，你还需要安装 Python 解释器。"
        ),
        (
            "大概需要多长时间才能学会？",
            "这取决于你的投入时间和学习目标。如果每天投入 2-3 小时，大约 2-3 个月可以掌握基础。但编程是持续学习的过程，重要的是坚持练习。"
        ),
    ]
    
    for user_msg, ai_msg in conversations:
        print(f"👤 用户: {user_msg}")
        print(f"🤖 AI: {ai_msg}")
        print()
        
        # 保存到内存（这里会调用 LLM 生成摘要）
        memory.save_context(
            {"input": user_msg},
            {"output": ai_msg}
        )
    
    # 查看生成的摘要
    print("\n" + "=" * 50)
    print("💾 生成的对话摘要：")
    print("=" * 50)
    history = memory.load_memory_variables({})
    print(history['history'])
    print("\n✨ 注意：完整的对话被压缩成了简洁的摘要！")


def demo_summary_vs_buffer():
    """对比摘要内存和普通缓冲内存"""
    print("\n" + "=" * 50)
    print("演示 2: 摘要内存 vs 完整历史对比")
    print("=" * 50)
    print("\n💡 这个演示展示两种内存方式的差异\n")
    
    # 准备测试数据
    conversations = [
        ("我叫张三，今年25岁", "你好张三！很高兴认识你。"),
        ("我是一名软件工程师", "很棒的职业！你主要使用什么技术栈？"),
        ("主要是 Python 和 JavaScript", "这两个都是非常流行的语言。"),
        ("我想学习人工智能", "AI 是个很有前景的方向！"),
    ]
    
    from langchain.memory import ConversationBufferMemory
    
    # 方式1: 普通缓冲内存
    buffer_memory = ConversationBufferMemory()
    for user_msg, ai_msg in conversations:
        buffer_memory.save_context(
            {"input": user_msg},
            {"output": ai_msg}
        )
    
    buffer_history = buffer_memory.load_memory_variables({})
    print("📦 ConversationBufferMemory (完整历史):")
    print(buffer_history['history'])
    print(f"\n字符数: {len(buffer_history['history'])}")
    
    # 方式2: 摘要内存（需要 API）
    print("\n" + "-" * 50)
    print("📄 ConversationSummaryMemory (摘要):")
    print("⚠️  需要 OpenAI API Key 才能生成摘要")
    print("如果配置了 API，取消注释下面的代码：")
    print("-" * 50)
    
    # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    # summary_memory = ConversationSummaryMemory(llm=llm)
    # for user_msg, ai_msg in conversations:
    #     summary_memory.save_context(
    #         {"input": user_msg},
    #         {"output": ai_msg}
    #     )
    # summary_history = summary_memory.load_memory_variables({})
    # print(summary_history['history'])
    # print(f"\n字符数: {len(summary_history['history'])}")


def demo_custom_prompt():
    """演示自定义摘要提示词"""
    print("\n" + "=" * 50)
    print("演示 3: 自定义摘要提示词")
    print("=" * 50)
    print("\n⚠️  此演示需要 OpenAI API Key\n")
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # 创建自定义的摘要提示词
    from langchain.prompts import PromptTemplate
    
    # 你可以自定义如何生成摘要
    # 默认提示词会生成一个渐进式的摘要
    memory = ConversationSummaryMemory(
        llm=llm,
        return_messages=False
    )
    
    print("💡 提示：你可以通过修改 prompt 来改变摘要的风格")
    print("例如：更简洁、更详细、侧重某些信息等\n")
    
    # 示例对话
    memory.save_context(
        {"input": "我计划下周去北京旅游"},
        {"output": "太好了！北京有很多著名景点，比如故宫、长城、天坛等。你计划去几天？"}
    )
    
    memory.save_context(
        {"input": "计划去3天，有什么建议吗？"},
        {"output": "3天的话，建议第一天去故宫和天安门，第二天去长城，第三天去颐和园和鸟巢。记得提前订票！"}
    )
    
    print("📄 生成的摘要：")
    print(memory.load_memory_variables({})['history'])


def demo_token_comparison():
    """演示 token 数量对比（概念演示）"""
    print("\n" + "=" * 50)
    print("演示 4: Token 使用量对比（概念）")
    print("=" * 50)
    
    print("""
    💡 为什么使用摘要内存？
    
    假设一个对话场景：
    - 完整对话: 10 轮 × 100 tokens/轮 = 1000 tokens
    - 摘要内存: 可能只需要 200-300 tokens
    
    好处：
    ✅ 节省 API 调用成本（按 token 计费）
    ✅ 避免超出模型的上下文长度限制
    ✅ 保留关键信息，去掉冗余内容
    
    权衡：
    ⚠️  需要额外的 LLM 调用来生成摘要（有成本）
    ⚠️  摘要可能丢失一些细节信息
    ⚠️  摘要质量取决于 LLM 的能力
    
    适用场景：
    - 超长对话（几十轮以上）
    - 客服历史记录
    - 会议纪要
    - 需要保留关键信息但控制成本
    """)


if __name__ == "__main__":
    print("🎓 LangChain Memory 教程 - ConversationSummaryMemory\n")
    
    # 演示2不需要API
    demo_summary_vs_buffer()
    
    # 演示4：概念讲解
    demo_token_comparison()
    
    print("\n" + "=" * 50)
    print("⚠️  以下演示需要 OpenAI API Key")
    print("请在代码中取消注释相关部分")
    print("=" * 50)
    # demo_summary_memory_basic()
    # demo_custom_prompt()
    
    print("\n" + "=" * 50)
    print("📚 知识点总结")
    print("=" * 50)
    print("""
    ConversationSummaryMemory 特点：
    ✅ 压缩对话历史，节省 tokens
    ✅ 保留关键信息
    ✅ 适合超长对话
    ❌ 需要额外的 LLM 调用（有成本）
    ❌ 可能丢失细节信息
    ❌ 摘要质量依赖 LLM 能力
    
    关键概念：
    - 使用 LLM 生成对话摘要
    - 摘要会随着对话不断更新
    - 可以自定义摘要的风格和重点
    
    💡 思考题：
    1. 什么场景下应该使用摘要内存而不是窗口内存？
    2. 如果对话每轮都生成摘要，成本会如何？
    3. 如何评估摘要的质量？
    """)

