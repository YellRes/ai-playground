"""
DeepSeek API 配置测试脚本
用于验证 API Key 是否配置正确
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("="*60)
print("🔍 DeepSeek API 配置测试")
print("="*60)

# 1. 检查环境变量
print("\n1️⃣ 检查环境变量...")
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    print("❌ 未找到 DEEPSEEK_API_KEY 环境变量")
    print("\n💡 解决方法：")
    print("1. 在当前目录创建 .env 文件")
    print("2. 添加以下内容：")
    print("   DEEPSEEK_API_KEY=your_actual_api_key")
    print("\n3. 重新运行此脚本")
    exit(1)
else:
    # 隐藏部分密钥以保护隐私
    masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "****"
    print(f"✅ 找到 API Key: {masked_key}")

# 2. 测试 Chat API
print("\n2️⃣ 测试 DeepSeek Chat API...")
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage
    
    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=api_key,
        openai_api_base="https://api.deepseek.com",
        temperature=0.7,
    )
    
    # 发送测试消息
    response = llm.invoke([HumanMessage(content="你好，请回复'测试成功'")])
    print(f"✅ Chat API 测试成功！")
    print(f"   响应: {response.content}")
    
except Exception as e:
    print(f"❌ Chat API 测试失败: {str(e)}")
    print("\n💡 可能的原因：")
    print("1. API Key 无效或已过期")
    print("2. 网络连接问题")
    print("3. API 服务暂时不可用")
    exit(1)

# 3. 测试 Embeddings API（可选）
print("\n3️⃣ 测试 DeepSeek Embeddings API...")
try:
    from langchain_openai import OpenAIEmbeddings
    
    embeddings = OpenAIEmbeddings(
        openai_api_key=api_key,
        openai_api_base="https://api.deepseek.com"
    )
    
    # 测试向量化
    test_vectors = embeddings.embed_documents(["测试文本"])
    print(f"✅ Embeddings API 测试成功！")
    print(f"   向量维度: {len(test_vectors[0])}")
    
except Exception as e:
    print(f"⚠️  Embeddings API 测试失败: {str(e)}")
    print("\n💡 说明：")
    print("DeepSeek 可能不支持 Embeddings API")
    print("这不影响基本的对话功能，但会影响 PDF 向量检索功能")
    print("\n可选解决方案：")
    print("1. 使用 OpenAI 的 Embeddings（需要额外的 OpenAI API Key）")
    print("2. 使用本地 Embeddings 模型（如 HuggingFace）")
    print("3. 仅使用文本提取功能，不使用向量检索")

print("\n" + "="*60)
print("✅ 测试完成！")
print("="*60)
print("\n💡 下一步：")
print("如果 Chat API 测试成功，您可以运行主程序：")
print("  python index.py              # 基础示例")
print("  python index.py interactive  # 交互式模式")

