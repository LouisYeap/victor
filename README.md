# Victor 🧰

> A general-purpose Python utility library — covering parallel execution, file I/O, and common development helpers.

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

Runtime dependencies:

| Package | Version | Purpose |
|---------|---------|---------|
| tqdm | ≥4.67 | Progress bars |
| PyYAML | ≥6.0 | YAML parsing |

---

## 📁 Project Structure

```
victor/
├── __init__.py            # Unified exports — all public APIs via victor.xxx
├── accelerate_util.py     # Thread / process pool parallel task execution
├── file_utils.py          # JSON / YAML / TXT / JSONL file I/O
├── command_utils.py       # Shell command execution
├── dz_util.py             # Date/list splitting, OBS URL parsing utilities
├── tool_types.py          # Type aliases & constants
├── tests/
│   └── test_victor.py     # Unit tests (35 cases)
└── README.md
```

---

## 🚀 Quick Start

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

# ── Thread pool (I/O-bound tasks) ───────────────
def fetch(url):
    import requests
    return requests.get(url).json()

results = thread_pool_executor(
    fetch,
    ["https://api.example.com/1", "https://api.example.com/2"],
    pool_size=10,
)
print(results["results"])

# ── Process pool (CPU-bound tasks) ───────────────
def calc(x):
    return x ** 3

results = process_pool_executor(calc, [1, 2, 3, 4, 5], pool_size=4)
print(results["results"])  # [1, 8, 27, 64, 125]

# ── File I/O ─────────────────────────────────────
save_json_to({"name": "victor", "version": "1.0.0"}, "./data", "config.json", indent=2)
config = load_json_from("./data/config.json")

# ── Shell command ────────────────────────────────
execute_command("git status", switch=True)

# ── Folder operations ───────────────────────────
clean_or_create_folder("./temp_output")   # Remove and recreate

# ── List splitting ─────────────────────────────
chunks = split_list(list(range(100)), n=10)  # Split into 10 roughly equal parts
```

---

## 📖 API Reference

### `accelerate_util` — Parallel Task Execution

| Function | Description |
|----------|-------------|
| `thread_pool_executor(func, tasks, pool_size=60, desc)` | Thread pool parallel execution, returns `{'results': [], 'errors': []}` |
| `process_pool_executor(func, tasks, pool_size=None, desc)` | Process pool, auto-detects CPU cores |
| `install_all_requirements(root_dir=".")` | Recursively install all `requirements.txt` under a directory |
| `is_windows()` | Check if the current OS is Windows |
| `get_absolute_path(path)` | Convert to absolute path (Windows long-path aware) |
| `clean_or_create_folder(path)` | Remove and recreate a folder |
| `clean_folder(path)` | Delete a folder (if it exists) |
| `clean_file(path)` | Delete a file (if it exists) |
| `search(dir, pattern)` / `rsearch(dir, pattern)` | File search, non-recursive / recursive |
| `list_folders_of_path(path)` / `list_files_of_path(path)` | List subfolders / files |
| `rlist_jsons_of_path(path)` | Recursively find all JSON files |
| `break_list(lst, n)` | Split a list into chunks of at most `n` elements |
| `timing_decorator(func)` | Decorator that prints function execution time |
| `fuzzy_get_value(data, key_part)` | Fuzzy-match dict keys, return corresponding values |
| `fuzzy_get_keys(data, key_part)` | Fuzzy-match dict keys, return matched key names |

### `file_utils` — File I/O

| Function | Description |
|----------|-------------|
| `load_text_from(path)` | Read entire file as text |
| `load_text_generator(path)` | Read file line-by-line (generator) |
| `read_txt_to_list(path)` | Read txt file, one line per list element |
| `write_list_to_txt(path, lst, mode="w")` | Write list contents to a txt file |
| `append_to_file(path, content)` | Append content to end of file |
| `load_json_from(path)` | Load JSON, auto-detects dict or list |
| `load_object_json_from(path)` | Load JSON, raises if not a dict |
| `load_list_json_from(path)` | Load JSON, raises if not a list |
| `save_json_to(obj, folder, name, indent=4)` | Save JSON with indent and Unicode control |
| `read_jsonl(path)` | Read a JSONL (JSON Lines) file |
| `json_list_to_jsonl(lst, path)` | Write a list of JSON objects to JSONL |
| `load_yaml_from(path)` | Load YAML file as dict |
| `copy_file_to_folder(src, dst, name=None)` | Copy file to destination folder |

### `command_utils` — Shell

| Function | Description |
|----------|-------------|
| `execute_command(cmd, max_retries=1, switch=False)` | Run a shell command; returns stdout if `switch=True`, `None` on success, or the command string on failure |

### `dz_util` — Utilities

| Function | Description |
|----------|-------------|
| `get_obs_base_url(obs_url)` | Extract bucket base path from an OBS URL |
| `split_txt_file(path, n)` | Split a txt file into `n` roughly equal parts |
| `split_datetime(start, end, n)` | Split a date range into `n` equal periods |
| `split_list(lst, n)` | Split a list into `n` roughly equal parts |

### `tool_types` — Types & Constants

| Name | Description |
|------|-------------|
| `PathLike` | Type alias `str \| os.PathLike` |
| `IMAGE_FILE_EXTENSIONS` | List of 30+ common image file extensions |

---

## 🧪 Running Tests

```bash
pip install pytest tqdm pyyaml
python -m pytest tests/ -v
```

**35 test cases, all passing.** ✅

---

## 📄 License

MIT License
