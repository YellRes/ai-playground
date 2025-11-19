from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
import getpass
import os

# os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("sk-915b0213517e462b838b932e5e28b272")


file_path = "./nke-10k-2023.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

# 为中文文本优化的分隔符配置
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # 中文建议更小的块大小
    chunk_overlap=200,   # 适当的重叠保持上下文
    add_start_index=True,
)
all_splits = text_splitter.split_documents(docs)


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_store = InMemoryVectorStore(embeddings)
ids = vector_store.add_documents(documents=all_splits)

results = vector_store.similarity_search("How many distribution centers does Nike have in the US?")

print(results[0])


