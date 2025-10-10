"""
HackerNews 工具使用示例
这个文件展示了如何直接使用 HackerNews 工具，无需配置 Agent
"""

from index import search_hackernews, get_hackernews_top_stories, get_hackernews_story_details


def example_1_search():
    """示例1: 搜索特定主题的文章"""
    print("=" * 70)
    print("示例 1: 搜索 'Python' 相关文章")
    print("=" * 70)
    
    result = search_hackernews.invoke({
        "query": "Python",
        "num_results": 3
    })
    print(result)
    print("\n")


def example_2_top_stories():
    """示例2: 获取热门文章"""
    print("=" * 70)
    print("示例 2: 获取当前热门文章")
    print("=" * 70)
    
    result = get_hackernews_top_stories.invoke({
        "num_stories": 3
    })
    print(result)
    print("\n")


def example_3_story_details():
    """示例3: 获取特定文章详情"""
    print("=" * 70)
    print("示例 3: 先搜索文章，然后获取详情")
    print("=" * 70)
    
    # 先搜索获取文章ID
    print("步骤 1: 搜索 'AI' 相关文章...")
    search_result = search_hackernews.invoke({
        "query": "AI",
        "num_results": 1
    })
    print(search_result[:200] + "...\n")
    
    # 注意：这里演示如何使用，但需要从搜索结果中提取实际的 ID
    print("步骤 2: 假设我们从搜索结果中找到了文章 ID，获取详情...")
    print("(实际使用时需要解析搜索结果获取 objectID)\n")


def example_4_multiple_searches():
    """示例4: 批量搜索多个主题"""
    print("=" * 70)
    print("示例 4: 批量搜索多个主题")
    print("=" * 70)
    
    topics = ["Machine Learning", "Web3", "Rust"]
    
    for topic in topics:
        print(f"\n🔍 搜索主题: {topic}")
        print("-" * 50)
        result = search_hackernews.invoke({
            "query": topic,
            "num_results": 2
        })
        # 只显示前300个字符
        print(result[:300] + "...\n")


def example_5_custom_usage():
    """示例5: 自定义使用场景"""
    print("=" * 70)
    print("示例 5: 实用场景 - 技术新闻摘要")
    print("=" * 70)
    
    print("\n📊 今日技术新闻摘要\n")
    
    # 1. 获取热门文章
    print("🔥 今日热门:")
    top_stories = get_hackernews_top_stories.invoke({"num_stories": 2})
    print(top_stories)
    
    # 2. 搜索特定技术
    print("\n" + "=" * 70)
    print("🔍 AI 领域最新动态:")
    ai_news = search_hackernews.invoke({"query": "AI", "num_results": 2})
    print(ai_news)


def main():
    """运行所有示例"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "HackerNews 工具使用示例" + " " * 22 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")
    
    examples = [
        ("1", "搜索文章", example_1_search),
        ("2", "热门文章", example_2_top_stories),
        ("3", "文章详情", example_3_story_details),
        ("4", "批量搜索", example_4_multiple_searches),
        ("5", "实用场景", example_5_custom_usage),
    ]
    
    print("可用示例:")
    for num, desc, _ in examples:
        print(f"  {num}. {desc}")
    print("  0. 运行所有示例")
    print()
    
    choice = input("请选择要运行的示例 (0-5): ").strip()
    print("\n")
    
    if choice == "0":
        for _, _, func in examples:
            func()
            print("\n" + "=" * 70 + "\n")
    else:
        for num, _, func in examples:
            if choice == num:
                func()
                break
        else:
            print("❌ 无效的选择！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序已退出！")
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")

