# Victor 🧰

> General-purpose Python utility library — covering parallel execution, file I/O, and common development helpers.

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Release](https://github.com/LouisYeap/victor/actions/workflows/release.yml/badge.svg)](https://github.com/LouisYeap/victor/actions/workflows/release.yml)
[![Tests](https://github.com/LouisYeap/victor/actions/workflows/test.yml/badge.svg)](https://github.com/LouisYeap/victor/actions/workflows/test.yml)

---

---

## 📦 Installation

```bash
pip install victor-utils
# or install from source
pip install -e .
```

---

## 📁 Project Structure

```
victor/
├── src/victor/
│   ├── __init__.py          # Unified public API — import everything from victor
│   ├── __init__.pyi         # Stub for cleaner IDE support (optional)
│   ├── accel.py             # Thread / process pool execution + path utilities
│   ├── command.py           # Shell command execution
│   ├── dz.py                # Date splitting & OBS URL utilities
│   ├── errors.py            # Custom exception hierarchy
│   ├── file.py              # JSON / YAML / TXT / JSONL file I/O
│   ├── types.py             # Public type aliases
│   ├── version.py           # Single source of truth for __version__
│   ├── _internal/           # Private implementation (not part of public API)
│   │   ├── __init__.py
│   │   ├── accel.py         # Internal acceleration utilities
│   │   └── typing.py        # Internal typing utilities
│   └── py.typed             # PEP 561 marker — package is typed
│
├── tests/
│   ├── conftest.py          # pytest path setup
│   └── test_victor.py      # 35 unit tests (all passing)
│
├── pyproject.toml           # Hatchling build configuration
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

# ── Thread pool (I/O-bound) ───────────────
def fetch(url):
    import requests
    return requests.get(url).json()

results = thread_pool_executor(
    fetch,
    ["https://api.example.com/1", "https://api.example.com/2"],
    pool_size=10,
)
print(results["results"])

# ── Process pool (CPU-bound) ───────────────
results = process_pool_executor(lambda x: x ** 3, [1, 2, 3, 4, 5], pool_size=4)
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

### `victor.accel` — Parallel Task Execution

| Function | Description |
|----------|-------------|
| `thread_pool_executor(func, tasks, pool_size=60, desc)` | Thread pool parallel execution; returns `{'results': [], 'errors': []}` |
| `process_pool_executor(func, tasks, pool_size=None, desc)` | Process pool; auto-detects CPU cores |
| `install_all_requirements(root_dir=".")` | Recursively install all `requirements.txt` |
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
| `fuzzy_get_value(data, key_part)` | Fuzzy-match dict keys, return values |
| `fuzzy_get_keys(data, key_part)` | Fuzzy-match dict keys |

### `victor.file` — File I/O

| Function | Description |
|----------|-------------|
| `load_text_from(path)` | Read entire file as text |
| `load_text_generator(path)` | Read file line-by-line (generator) |
| `read_txt_to_list(path)` | Read txt, one line per list element |
| `write_list_to_txt(path, lst, mode="w")` | Write list contents to txt |
| `append_to_file(path, content)` | Append content to end of file |
| `load_json_from(path)` | Load JSON; auto-detects dict or list |
| `load_object_json_from(path)` | Load JSON; raises if not a dict |
| `load_list_json_from(path)` | Load JSON; raises if not a list |
| `save_json_to(obj, folder, name, indent=4)` | Save JSON with indent and Unicode control |
| `read_jsonl(path)` | Read a JSONL (JSON Lines) file |
| `json_list_to_jsonl(lst, path)` | Write a list of JSON objects to JSONL |
| `load_yaml_from(path)` | Load YAML file as dict |
| `copy_file_to_folder(src, dst, name=None)` | Copy file to destination folder |

### `victor.command` — Shell

| Function | Description |
|----------|-------------|
| `execute_command(cmd, max_retries=1, switch=False)` | Run a shell command; returns stdout if `switch=True`, `None` on success, or the command string on failure |

### `victor.dz` — Utilities

| Function | Description |
|----------|-------------|
| `get_obs_base_url(obs_url)` | Extract bucket base path from an OBS URL |
| `split_txt_file(path, n)` | Split a txt file into `n` roughly equal parts |
| `split_datetime(start, end, n)` | Split a date range into `n` equal periods |
| `split_list(lst, n)` | Split a list into `n` roughly equal parts |

### `victor.errors` — Exceptions

| Class | Description |
|-------|-------------|
| `VictorError` | Base exception for all Victor errors |
| `ErrorCode` | Enum of error codes for programmatic handling |
| `FileNotFoundError` | Raised when a required file does not exist |
| `InvalidJSONError` | Raised when JSON decoding fails |
| `InvalidYAMLError` | Raised when YAML parsing fails |
| `InvalidTypeError` | Raised when a value has an unexpected type |
| `CommandFailedError` | Raised when a shell command fails |
| `ParallelExecutionError` | Raised when parallel tasks fail |

### `victor.types` — Types

| Name | Description |
|------|-------------|
| `PathLike` | Type alias `str \| os.PathLike` |

---

## 🧪 Running Tests

```bash
pip install -e ".[dev]"
python -m pytest tests/ -v
```

**35 test cases, all passing.** ✅

---

## 📥 Downloads

Pre-built wheels for Windows, macOS, and Linux are available in the [Releases](https://github.com/LouisYeap/victor/releases).

| Platform | File |
|----------|------|
| Windows | `victor_utils-*-win_amd64.whl` |
| macOS (Intel) | `victor_utils-*-macosx_10_9_x86_64.macosx_11_0_arm64.macosx_10_9_universal2.whl` |
| Linux | `victor_utils-*-manylinux_*_x86_64.whl` |

---

## 📄 License

MIT License
