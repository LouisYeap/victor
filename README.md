# 📦 Victor Utility Library

Victor 是一个 Python 工具库，提供多线程/多进程处理、文件操作、数学计算等实用工具。

---

## 📌 目录结构

```
victor/
├── accelerate_util.py      # 多线程 & 多进程任务处理工具
├── async_file_utils.py     # 异步文件操作工具
├── command_utils.py        # 执行 shell 命令的工具
├── file_utils.py           # 同步文件操作工具
├── tool_math.py            # 数学 & 几何计算工具
├── tool_types.py           # 常用类型 & 常量定义
├── utils.py                # 其他实用工具
├── README.md               # 说明文档
├── requirements.txt        # 依赖包列表
```

---

## 🔧 安装

```bash
pip install -r requirements.txt
```

---

## 🚀 使用示例

### 1️⃣ **多线程/多进程任务处理**（`accelerate_util.py`）
```python
from victor.accelerate_util import thread_pool_executor

def task(x):
    return x * x

results = thread_pool_executor(task, [1, 2, 3, 4, 5], pool_size=4)
print(results)
```

### 2️⃣ **执行 Shell 命令**（`command_utils.py`）
```python
from victor.command_utils import execute_command

execute_command("ls -l", switch=True)
```

### 3️⃣ **文件操作**（`file_utils.py` & `async_file_utils.py`）
```python
from victor.file_utils import read_file, write_file

write_file("test.txt", "Hello, Victor!")
print(read_file("test.txt"))
```

---

## 📜 依赖
  pipreqs . --force    # 生成 requirements.txt 
- Python 3.7+
- tqdm
- numpy
- pymongo（如果需要数据库支持）

---

## 📝 贡献
欢迎提交 PR 或 Issue，帮助改进 Victor！

---

## 📄 许可证
MIT License
