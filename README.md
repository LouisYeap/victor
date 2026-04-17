# Victor 🧰

> Python 通用工具库 — 涵盖并行处理、文件操作、日志工具等日常开发常用模块。

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📦 安装

```bash
pip install -r requirements.txt
```

仅有两个运行时依赖：

| 包 | 版本 | 用途 |
|---|---|---|
| tqdm | ≥4.67 | 进度条 |
| PyYAML | ≥6.0 | YAML 解析 |

---

## 📁 目录结构

```
victor/
├── __init__.py            # 统一导出，所有公共 API 均通过 victor.xxx 调用
├── accelerate_util.py     # 多线程 / 多进程并行任务处理
├── file_utils.py          # JSON / YAML / TXT / JSONL 文件读写
├── command_utils.py       # Shell 命令执行
├── dz_util.py             # 日期列表拆分、OBS URL 解析等业务工具
├── tool_types.py          # 类型别名 & 常量定义
├── tests/
│   └── test_victor.py     # 单元测试（35 个用例）
└── README.md
```

---

## 🚀 快速开始

```python
from victor import (
    thread_pool_executor,
    process_pool_executor,
    save_json_to,
    load_json_from,
    execute_command,
    clean_or_create_folder,
    split_list,
)

# ── 并行处理（线程池，适合 I/O 密集型）──
def fetch(url):
    import requests
    return requests.get(url).json()

results = thread_pool_executor(
    fetch,
    ["https://api.example.com/1", "https://api.example.com/2"],
    pool_size=10,
)
print(results["results"])

# ── 并行处理（进程池，适合 CPU 密集型）──
def calc(x):
    return x ** 3

results = process_pool_executor(calc, [1, 2, 3, 4, 5], pool_size=4)
print(results["results"])  # [1, 8, 27, 64, 125]

# ── 文件读写 ────────────────────────────
save_json_to({"name": "victor", "version": "1.0.0"}, "./data", "config.json", indent=2)
config = load_json_from("./data/config.json")

# ── 执行 Shell 命令 ────────────────────
execute_command("git status", switch=True)

# ── 文件夹操作 ─────────────────────────
clean_or_create_folder("./temp_output")   # 先删后建

# ── 列表拆分 ───────────────────────────
chunks = split_list(list(range(100)), n=10)  # 均分成 10 份
```

---

## 📖 API 文档

### `accelerate_util` — 并行任务处理

| 函数 | 说明 |
|---|---|
| `thread_pool_executor(func, tasks, pool_size=60, desc)` | 线程池并行，返回 `{'results': [], 'errors': []}` |
| `process_pool_executor(func, tasks, pool_size=None, desc)` | 进程池并行，自动匹配 CPU 核心数 |
| `install_all_requirements(root_dir=".")` | 递归安装目录下所有 requirements.txt |
| `is_windows()` | 判断当前系统是否为 Windows |
| `get_absolute_path(path)` | 获取绝对路径（Windows 长路径兼容） |
| `clean_or_create_folder(path)` | 先删后建文件夹 |
| `clean_folder(path)` | 删除文件夹 |
| `clean_file(path)` | 删除文件 |
| `search(dir, pattern)` / `rsearch(dir, pattern)` | 文件搜索（非递归 / 递归） |
| `list_folders_of_path(path)` / `list_files_of_path(path)` | 列出子文件夹 / 文件 |
| `rlist_jsons_of_path(path)` | 递归获取所有 JSON 文件 |
| `break_list(lst, n)` | 将列表均分成每份最多 n 个元素 |
| `timing_decorator(func)` | 打印函数执行耗时的装饰器 |
| `fuzzy_get_value(data, key_part)` | 模糊匹配 key，返回 value 列表 |
| `fuzzy_get_keys(data, key_part)` | 模糊匹配 key，返回 key 列表 |

### `file_utils` — 文件读写

| 函数 | 说明 |
|---|---|
| `load_text_from(path)` | 一次性读取文本 |
| `load_text_generator(path)` | 逐行读取（生成器） |
| `read_txt_to_list(path)` | 读取 txt，每行作为列表元素 |
| `write_list_to_txt(path, lst, mode="w")` | 列表写入 txt |
| `append_to_file(path, content)` | 追加内容到文件末尾 |
| `load_json_from(path)` | 加载 JSON（自动识别 dict/list） |
| `load_object_json_from(path)` | 加载 JSON，仅接受 dict |
| `load_list_json_from(path)` | 加载 JSON，仅接受 list |
| `save_json_to(obj, folder, name, indent=4)` | 保存 JSON，支持缩进和 Unicode 控制 |
| `read_jsonl(path)` | 读取 JSONL 文件 |
| `json_list_to_jsonl(lst, path)` | 写入 JSONL 文件 |
| `load_yaml_from(path)` | 加载 YAML 为 dict |
| `copy_file_to_folder(src, dst, name=None)` | 复制文件到目标文件夹 |

### `command_utils` — Shell 命令

| 函数 | 说明 |
|---|---|
| `execute_command(cmd, max_retries=1, switch=False)` | 执行命令，失败返回命令字符串 |

### `dz_util` — 业务工具

| 函数 | 说明 |
|---|---|
| `get_obs_base_url(obs_url)` | 从 OBS URL 提取 bucket 基础路径 |
| `split_txt_file(path, n)` | 将 txt 均分 n 份 |
| `split_datetime(start, end, n)` | 按日期区间均分 n 段 |
| `split_list(lst, n)` | 将列表均分 n 份 |

### `tool_types` — 类型 & 常量

| 名称 | 说明 |
|---|---|
| `PathLike` | `str | os.PathLike` 类型别名 |
| `IMAGE_FILE_EXTENSIONS` | 常见图片扩展名列表（30+ 种） |

---

## 🧪 运行测试

```bash
pip install pytest tqdm pyyaml
python -m pytest tests/ -v
```

当前测试覆盖率：**35 个用例，全部通过**。

---

## 📄 许可证

MIT License
