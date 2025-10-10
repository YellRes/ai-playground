# LangChain 自定义工具教程

这个目录包含了如何在 LangChain 中创建和使用自定义工具的完整示例。

## 文件说明

### 📁 文件结构
```
demo-hacknew/
├── quick_start.py    # 快速入门示例（推荐先看这个）
├── tools.py         # 详细的工具示例集合
├── index.py         # 完整的演示程序
└── README.md        # 本说明文档
```

### 📖 学习路径

1. **quick_start.py** - 最简单的入门示例
   - 创建基本的自定义工具
   - 快速上手，适合初学者

2. **tools.py** - 各种类型的工具示例
   - 6种不同类型的自定义工具
   - 包含错误处理和数据验证
   - 实际应用场景示例

3. **index.py** - 高级用法和完整演示
   - 使用 Pydantic 模型定义工具参数
   - StructuredTool 的使用方法
   - 交互式测试界面

## 🛠️ 自定义工具的5种创建方法

### 方法 1: 基本 @tool 装饰器
```python
from langchain_core.tools import tool

@tool
def my_tool(param: str) -> str:
    \"\"\"工具描述\"\"\"
    return f"处理结果: {param}"
```

### 方法 2: 带参数模型的工具
```python
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    text: str = Field(description="输入文本")
    mode: str = Field(description="处理模式", default="basic")

@tool(args_schema=MyToolInput)
def advanced_tool(text: str, mode: str = "basic") -> str:
    \"\"\"高级工具\"\"\"
    return f"以{mode}模式处理: {text}"
```

### 方法 3: 使用 StructuredTool
```python
from langchain_core.tools import StructuredTool

def my_function(input_str: str) -> str:
    return f"处理: {input_str}"

tool = StructuredTool.from_function(
    func=my_function,
    name="my_tool",
    description="我的工具描述"
)
```

### 方法 4: 错误处理的工具
```python
@tool
def safe_tool(input_data: str) -> str:
    \"\"\"带错误处理的安全工具\"\"\"
    try:
        # 处理逻辑
        result = process_data(input_data)
        return result
    except Exception as e:
        return f"处理失败: {str(e)}"
```

### 方法 5: 复杂数据处理工具
```python
@tool
def data_processor(data: str) -> str:
    \"\"\"处理复杂数据结构\"\"\"
    # 解析、验证、处理、返回
    # 支持JSON、CSV等格式
    return processed_result
```

## 🚀 快速开始

1. **安装依赖**
```bash
pip install langchain langchain-core langchain-deepseek
```

2. **设置API密钥**
```python
import os
os.environ["DEEPSEEK_API_KEY"] = "your-api-key-here"
```

3. **运行示例**
```bash
# 快速入门
python quick_start.py

# 完整演示  
python index.py

# 工具集合演示
python tools.py
```

## 📝 关键概念

### 工具的组成部分
1. **函数名**: 工具的标识符
2. **描述**: 帮助AI理解何时使用这个工具
3. **参数**: 工具需要的输入
4. **返回值**: 工具的输出结果

### 最佳实践
1. **清晰的描述**: 让AI知道什么时候使用你的工具
2. **参数验证**: 确保输入数据的正确性
3. **错误处理**: 优雅地处理异常情况
4. **类型提示**: 帮助IDE和运行时检查
5. **文档字符串**: 提供详细的使用说明

### 常见用途
- **数据库查询**: 从数据库获取信息
- **API调用**: 调用外部服务
- **文件操作**: 读写文件
- **计算任务**: 执行复杂计算
- **数据分析**: 处理和分析数据
- **系统集成**: 与其他系统交互

## 🔧 故障排除

### 常见问题
1. **工具没有被调用**: 检查工具描述是否清晰
2. **参数错误**: 确认参数类型和名称正确
3. **返回值问题**: 确保返回字符串类型
4. **API密钥错误**: 检查环境变量设置

### 调试技巧
- 在工具函数中添加打印语句
- 检查agent的工具列表
- 查看完整的错误堆栈信息

## 📚 进一步学习

- [LangChain 官方文档](https://docs.langchain.com/)
- [工具调用最佳实践](https://docs.langchain.com/oss/python/langchain/tools)
- [Agent 构建指南](https://docs.langchain.com/oss/python/langchain/agents)

---

💡 **提示**: 从 `quick_start.py` 开始，逐步学习更复杂的示例！








