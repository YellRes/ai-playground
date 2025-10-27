# 中文 PDF 优化说明

## 🎯 已完成的优化

### 1. PDF 加载器升级
- ✅ 从 `PyPDFLoader` 升级到 `PyMuPDFLoader`
- ✅ 更好的中文字符提取支持
- ✅ 更快的处理速度

### 2. 文本分割优化
- ✅ chunk_size: 1000 → 500（适应中文字符密度）
- ✅ chunk_overlap: 200 → 100
- ✅ 添加更多中文分隔符：`。！？；，`
- ✅ 使用字符数而非 token 数计算长度

### 3. Embeddings 模型升级
- ✅ 从 OpenAI Embeddings 改为本地中文模型
- ✅ 使用 `BAAI/bge-base-zh-v1.5` 中文优化模型
- ✅ 无需 API Key，完全本地运行
- ✅ 支持离线使用

## 📦 依赖安装

### 方案 A：在虚拟环境中安装（推荐）

```bash
# 1. 创建虚拟环境
cd langchain/financial-statements
python -m venv venv

# 2. 激活虚拟环境
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat

# 3. 安装依赖
pip install -r requirements.txt
```

### 方案 B：解决 Windows 长路径问题（全局安装）

如果您遇到 "No such file or directory" 错误，需要启用 Windows 长路径支持：

#### 方法 1：使用注册表编辑器
1. 按 `Win + R`，输入 `regedit`
2. 导航到：`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`
3. 找到 `LongPathsEnabled`，双击修改值为 `1`
4. 如果不存在，右键新建 DWORD (32位) 值，命名为 `LongPathsEnabled`，值设为 `1`
5. 重启电脑

#### 方法 2：使用管理员 PowerShell（推荐）
```powershell
# 以管理员身份运行 PowerShell，执行：
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

#### 方法 3：使用组策略（Windows 10 1607+）
1. 按 `Win + R`，输入 `gpedit.msc`
2. 导航到：计算机配置 → 管理模板 → 系统 → 文件系统
3. 双击"启用 Win32 长路径"
4. 选择"已启用"
5. 重启电脑

### 方案 C：手动安装依赖

```bash
# 按顺序安装（避免长路径问题）
pip install pymupdf
pip install sentence-transformers --no-deps
pip install transformers huggingface-hub tokenizers safetensors
pip install scikit-learn scipy
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

## 🚀 使用方法

### 1. 测试 PDF 加载

```python
from langchain_community.document_loaders import PyMuPDFLoader

# 加载 PDF
loader = PyMuPDFLoader("600006_20250830_WOQW.pdf")
documents = loader.load()

# 查看提取结果
print(f"页数: {len(documents)}")
print(f"前100字: {documents[0].page_content[:100]}")
```

### 2. 运行完整的财务分析

```bash
# 交互式模式
python index.py interactive

# PDF 分析模式
python index.py pdf
```

### 3. 在代码中使用

```python
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyMuPDFLoader

# 加载 PDF
loader = PyMuPDFLoader("600006_20250830_WOQW.pdf")
documents = loader.load()

# 创建中文 Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-zh-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

# 创建向量数据库
vectorstore = FAISS.from_documents(documents, embeddings)

# 检索
results = vectorstore.similarity_search("营业收入", k=3)
for doc in results:
    print(doc.page_content)
```

## 📊 模型信息

### BAAI/bge-base-zh-v1.5
- **来源**: 北京智源人工智能研究院（BAAI）
- **大小**: 约 400 MB
- **维度**: 768
- **特点**: 专门针对中文优化，在中文检索任务上表现优异
- **首次运行**: 会自动从 HuggingFace 下载模型

### 模型下载加速（可选）

如果下载慢，可以设置国内镜像：

```bash
# 设置 HuggingFace 镜像
set HF_ENDPOINT=https://hf-mirror.com
# 或
$env:HF_ENDPOINT="https://hf-mirror.com"

# 然后再运行程序
python index.py
```

## 🔧 其他中文 Embedding 模型选择

如果需要更快或更小的模型，可以修改 `index.py` 中的模型名称：

```python
# 轻量级（更快，约 200 MB）
model_name="BAAI/bge-small-zh-v1.5"

# 大型模型（更准确，约 1.3 GB）
model_name="BAAI/bge-large-zh-v1.5"

# 其他优秀的中文模型
model_name="moka-ai/m3e-base"  # 通用型
model_name="shibing624/text2vec-base-chinese"  # 经典选择
```

## ⚠️ 注意事项

### 1. PDF 类型识别
- **文字型 PDF**: PyMuPDFLoader 可以直接提取 ✅
- **扫描型 PDF**: 需要 OCR 识别，参考 `使用说明.md` 中的 OCR 方案

### 2. 首次运行
- 首次运行会下载 Embedding 模型（约 400 MB）
- 请确保网络连接正常
- 下载完成后会缓存到本地，后续无需重新下载

### 3. 内存要求
- 最小内存: 4 GB
- 推荐内存: 8 GB 以上
- 如果内存不足，可以使用 `bge-small-zh-v1.5` 模型

### 4. GPU 加速（可选）
如果您有 NVIDIA GPU，可以修改为使用 GPU 加速：

```python
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-zh-v1.5",
    model_kwargs={'device': 'cuda'},  # 改为 cuda
    encode_kwargs={'normalize_embeddings': True}
)
```

## 🆚 优化前后对比

| 项目 | 优化前 | 优化后 |
|------|--------|--------|
| PDF 加载器 | PyPDFLoader | PyMuPDFLoader |
| 中文支持 | 一般 | 优秀 |
| Embeddings | DeepSeek API（不支持） | 本地中文模型 |
| API Key | 需要 | 不需要 |
| 网络要求 | 必须联网 | 离线可用（首次需下载模型） |
| 成本 | API 调用费用 | 免费 |
| chunk_size | 1000 | 500（更适合中文） |
| 中文分隔符 | 基础 | 完整（含；，等） |

## 📝 更新日志

### 2025-10-09
- ✅ 升级到 PyMuPDFLoader
- ✅ 集成 BAAI/bge-base-zh-v1.5 中文模型
- ✅ 优化文本分割策略
- ✅ 添加详细的进度提示
- ✅ 更新依赖配置

## 🤝 技术支持

如有问题，请检查：
1. Python 版本 >= 3.8
2. 虚拟环境是否正确激活
3. 依赖包是否完整安装
4. Windows 长路径支持是否启用
5. 网络连接是否正常（首次运行）

## 📚 相关文档

- [快速开始.md](./快速开始.md) - 基础使用教程
- [使用说明.md](./使用说明.md) - 完整功能说明
- [环境配置说明.md](./环境配置说明.md) - 环境配置指南

