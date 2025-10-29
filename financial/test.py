from index import create_financial_agent
from run_browser import run_browser
from download_pdf import download_pdf
from langchain_core.messages import HumanMessage

def test():
    pdf_path = run_browser('600032')

    download_pdf(pdf_path[0].get('url'), f"{pdf_path[0].get('name')}.pdf")

     # 创建 agent
    agent, system_message = create_financial_agent()
    
    # PDF文件路径
    # pdf_path = "./603259_20250729_Z1D5.pdf"
    
    # 测试查询
    test_queries = [
        f"请加载并分析这个PDF文件：./pdf/{pdf_path[0].get('name')}.pdf",
        "从PDF中提取所有关键财务数据",
        "基于提取的数据，分析这家公司的整体财务状况",
    ]
    
    thread_id = "pdf_analysis_session"
    config = {"configurable": {"thread_id": thread_id}}
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"📝 问题 {i}: {query}")
        print(f"{'='*60}\n")
        
        # 第一次对话时包含系统消息
        if i == 1:
            messages = [system_message, HumanMessage(content=query)]
        else:
            messages = [HumanMessage(content=query)]
        
        result = agent.invoke(
            {"messages": messages},
            config=config
        )
        
        # 显示回复
        last_message = result['messages'][-1]
        print(f"🤖 AI: {last_message.content}\n")