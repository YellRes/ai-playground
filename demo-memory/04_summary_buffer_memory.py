"""
LangChain Memory 示例 4: ConversationSummaryBufferMemory
=========================================================
摘要缓冲内存：结合摘要和窗口的优点
- 保留最近的完整对话
- 对较早的对话生成摘要
适用场景：既需要最新完整上下文，又要控制总 token 数量
"""

from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI

def demo_summary_buffer_basic():
    """演示摘要缓冲内存的基本概念"""
    print("=" * 50)
    print("演示 1: 理解 SummaryBuffer 的工作原理")
    print("=" * 50)
    
    print("""
    💡 ConversationSummaryBufferMemory 如何工作：
    
    1. 设定一个 token 限制（max_token_limit）
    2. 最近的消息保持完整形式
    3. 当消息超出 token 限制时，较早的消息被总结
    4. 最终内存 = 摘要 + 最近的完整消息
    
    示意图：
    ┌─────────────────────────────────────┐
    │  早期对话 → 被压缩成摘要            │
    ├─────────────────────────────────────┤
    │  最近的对话 → 保持完整              │
    └─────────────────────────────────────┘
    
    这样的好处：
    ✅ 有完整的近期上下文（重要！）
    ✅ 有早期对话的关键信息
    ✅ 总 token 数量可控
    """)


def demo_with_api():
    """演示实际使用（需要 API）"""
    print("\n" + "=" * 50)
    print("演示 2: 实际使用示例")
    print("=" * 50)
    print("\n⚠️  此演示需要 OpenAI API Key\n")
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # 设置 token 限制为 200
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=200  # 超过这个限制就开始总结
    )
    
    print("📝 添加多轮对话：\n")
    
    conversations = [
        (
            "我正在准备一个项目演讲",
            "太好了！演讲是展示项目成果的重要方式。你的项目是关于什么的？"
        ),
        (
            "是关于使用 AI 优化客户服务的项目",
            "这是个很有价值的应用方向！AI 可以大大提升客服效率和用户体验。你们具体用了哪些技术？"
        ),
        (
            "主要使用了自然语言处理和机器学习",
            "NLP 和 ML 是 AI 客服的核心技术。你们训练了自己的模型还是使用了现有的 API？"
        ),
        (
            "我们使用了 OpenAI 的 API 和一些开源模型",
            "这是个不错的组合。OpenAI API 提供强大的基础能力，开源模型可以针对特定需求调优。"
        ),
        (
            "演讲时间只有 10 分钟，该重点讲什么？",
            "10 分钟的话，建议重点讲：1) 问题背景和解决方案 2) 核心技术架构 3) 实际效果数据。技术细节可以简化。"
        ),
        (
            "好的，我需要准备什么样的演示材料？",
            "建议准备：1) 简洁的 PPT（不超过 10 页）2) 实际系统的演示视频或 Demo 3) 效果对比数据图表。"
        ),
    ]
    
    for i, (user_msg, ai_msg) in enumerate(conversations, 1):
        print(f"轮次 {i}:")
        print(f"  👤 {user_msg}")
        print(f"  🤖 {ai_msg}\n")
        
        memory.save_context(
            {"input": user_msg},
            {"output": ai_msg}
        )
        
        # 每两轮显示一次内存状态
        if i % 2 == 0:
            print(f"  💾 当前内存状态（第 {i} 轮后）：")
            history = memory.load_memory_variables({})
            print(f"  {history['history'][:200]}...")
            print(f"  总字符数: {len(history['history'])}")
            print("  " + "-" * 40 + "\n")


def demo_token_limit_comparison():
    """对比不同 token 限制的效果"""
    print("\n" + "=" * 50)
    print("演示 3: 不同 Token 限制的影响")
    print("=" * 50)
    
    print("""
    💡 max_token_limit 参数的影响：
    
    情况1: max_token_limit = 50 (很小)
    → 只保留最近 1-2 轮完整对话
    → 其余都被总结
    → 适合：需要严格控制成本的场景
    
    情况2: max_token_limit = 500 (中等)
    → 保留最近 5-10 轮完整对话
    → 早期对话被总结
    → 适合：大多数应用场景
    
    情况3: max_token_limit = 2000 (较大)
    → 保留较多完整对话
    → 只有很早的对话被总结
    → 适合：需要丰富上下文的场景
    
    ⚠️  注意：token 计算基于模型的 tokenizer
    不同模型的 token 计算方式可能不同！
    """)


def demo_comparison_all_types():
    """对比所有 Memory 类型"""
    print("\n" + "=" * 50)
    print("演示 4: 四种 Memory 类型全面对比")
    print("=" * 50)
    
    print("""
    📊 四种 Memory 类型对比：
    
    1️⃣  ConversationBufferMemory
        保存: 所有对话完整历史
        优点: 信息完整、实现简单
        缺点: 无限增长、可能超限
        适用: 短对话、测试开发
    
    2️⃣  ConversationBufferWindowMemory
        保存: 最近 K 轮完整对话
        优点: 大小可控、不会超限
        缺点: 丢失早期信息
        适用: 长对话、只需近期上下文
    
    3️⃣  ConversationSummaryMemory
        保存: 整个历史的摘要
        优点: 压缩效率高、保留关键信息
        缺点: 需要 LLM 调用、可能丢失细节
        适用: 超长对话、需要历史概要
    
    4️⃣  ConversationSummaryBufferMemory ⭐
        保存: 摘要 + 最近完整对话
        优点: 兼顾效率和完整性
        缺点: 实现复杂、需要 LLM 调用
        适用: 生产环境、平衡性能和效果
    
    💡 选择建议：
    - 快速原型: BufferMemory
    - 成本敏感: WindowMemory
    - 需要历史: SummaryMemory
    - 生产环境: SummaryBufferMemory ⭐
    """)


def demo_practical_scenario():
    """实际场景示例"""
    print("\n" + "=" * 50)
    print("演示 5: 实际应用场景")
    print("=" * 50)
    
    print("""
    🎯 场景：在线教育辅导机器人
    
    需求分析：
    - 对话可能很长（20+ 轮）
    - 需要记住学生的基本信息（姓名、年级等）
    - 需要记住当前学习主题的详细上下文
    - 不需要记住很早之前的闲聊内容
    
    解决方案：ConversationSummaryBufferMemory
    - max_token_limit=400
    - 保留最近 5-8 轮完整对话（当前学习内容）
    - 总结早期对话（学生背景信息）
    
    效果：
    ✅ 机器人记得学生的基本信息
    ✅ 对当前问题有完整的上下文
    ✅ 不会因为对话太长而超出限制
    ✅ 成本可控
    
    代码示例（需要 API）：
    
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=400,
        return_messages=True  # 返回消息对象
    )
    
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )
    """)


if __name__ == "__main__":
    print("🎓 LangChain Memory 教程 - ConversationSummaryBufferMemory\n")
    
    # 运行概念演示（不需要 API）
    demo_summary_buffer_basic()
    demo_token_limit_comparison()
    demo_comparison_all_types()
    demo_practical_scenario()
    
    print("\n" + "=" * 50)
    print("⚠️  需要 OpenAI API Key 的演示")
    print("请在代码中取消注释")
    print("=" * 50)
    # demo_with_api()
    
    print("\n" + "=" * 50)
    print("📚 知识点总结")
    print("=" * 50)
    print("""
    ConversationSummaryBufferMemory 特点：
    ✅ 最佳平衡：完整性 + 效率
    ✅ 保留最近的完整上下文
    ✅ 保留早期的关键信息
    ✅ Token 数量可控
    ❌ 实现相对复杂
    ❌ 需要 LLM 调用生成摘要
    
    关键参数：
    - llm: 用于生成摘要的语言模型
    - max_token_limit: token 限制阈值
    - return_messages: 返回消息对象还是字符串
    
    适用场景：
    ✨ 生产环境的首选方案
    - 中长对话应用
    - 需要历史信息的客服
    - 在线教育、咨询等场景
    
    💡 思考题：
    1. 为什么要同时保留摘要和完整消息？
    2. 如何确定合适的 max_token_limit 值？
    3. 在什么情况下这个方案比单纯的窗口内存更好？
    """)
