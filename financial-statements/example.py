"""
财务报表分析智能体 - 使用示例
"""

from index import create_financial_agent
import os

def example_pdf_analysis():
    """示例：分析PDF财报"""
    print("="*60)
    print("📊 示例：PDF财报分析")
    print("="*60)
    
    # 创建agent
    agent = create_financial_agent()
    
    # PDF文件路径
    pdf_path = "langchain/financial-statements/600006_20250830_WOQW.pdf"
    
    # 会话配置
    config = {"configurable": {"thread_id": "example_session"}}
    
    # 示例1: 加载PDF
    print("\n【示例1】加载PDF财报\n")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": f"请加载这个PDF文件：{pdf_path}"}]},
        config=config
    )
    print(result['messages'][-1].content)
    
    # 示例2: 提取财务数据
    print("\n" + "="*60)
    print("【示例2】提取关键财务数据\n")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "提取所有关键财务数据"}]},
        config=config
    )
    print(result['messages'][-1].content)
    
    # 示例3: 综合分析
    print("\n" + "="*60)
    print("【示例3】综合财务分析\n")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "基于提取的数据，请给出这家公司的综合财务分析"}]},
        config=config
    )
    print(result['messages'][-1].content)
    
    # 示例4: 特定查询
    print("\n" + "="*60)
    print("【示例4】查询特定信息\n")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "这家公司的营业收入是多少？同比增长情况如何？"}]},
        config=config
    )
    print(result['messages'][-1].content)


def example_manual_analysis():
    """示例：手动输入数据进行分析"""
    print("\n\n" + "="*60)
    print("📊 示例：手动数据分析")
    print("="*60)
    
    # 创建agent
    agent = create_financial_agent()
    
    # 新会话
    config = {"configurable": {"thread_id": "manual_session"}}
    
    # 示例：分析盈利能力
    print("\n【示例】盈利能力分析\n")
    query = """
    请分析以下公司的财务状况：
    - 营业收入：5000万元
    - 净利润：800万元
    - 总资产：12000万元
    - 流动资产：3000万元
    - 流动负债：2000万元
    - 现金：500万元
    - 存货：800万元
    """
    
    result = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    print(result['messages'][-1].content)


def example_step_by_step():
    """示例：逐步分析流程"""
    print("\n\n" + "="*60)
    print("📊 示例：逐步分析流程")
    print("="*60)
    
    # 创建agent
    agent = create_financial_agent()
    config = {"configurable": {"thread_id": "step_session"}}
    
    steps = [
        ("步骤1：计算ROE", "计算ROE：净利润是500万，股东权益是5000万"),
        ("步骤2：计算流动比率", "计算流动比率：流动资产3000万，流动负债2000万"),
        ("步骤3：评估结果", "根据以上两个指标，这家公司的财务状况如何？"),
    ]
    
    for title, query in steps:
        print(f"\n【{title}】\n")
        result = agent.invoke(
            {"messages": [{"role": "user", "content": query}]},
            config=config
        )
        print(result['messages'][-1].content)
        print("\n" + "-"*60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "pdf":
            # PDF分析示例
            example_pdf_analysis()
        elif sys.argv[1] == "manual":
            # 手动数据分析示例
            example_manual_analysis()
        elif sys.argv[1] == "step":
            # 逐步分析示例
            example_step_by_step()
        else:
            print("可用示例：")
            print("  python example.py pdf    - PDF财报分析")
            print("  python example.py manual - 手动数据分析")
            print("  python example.py step   - 逐步分析流程")
    else:
        # 运行所有示例
        print("🚀 运行所有示例...\n")
        example_pdf_analysis()
        example_manual_analysis()
        example_step_by_step()
        
        print("\n\n" + "="*60)
        print("✅ 所有示例运行完成！")
        print("="*60)

