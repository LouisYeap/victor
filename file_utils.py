"""文件读写工具（JSON / YAML / TXT / JSONL 等）"""

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

from .tool_types import PathLike


# ─────────────── TXT ───────────────


def load_text_from(file_path: PathLike) -> str:
    """一次性读取文件所有文本。"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_text_generator(file_path: PathLike):
    """逐行读取文件（生成器），节省内存。"""
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


def read_txt_to_list(txt_path: PathLike) -> List[str]:
    """读取 txt 文件，每行作为列表一个元素。"""
    return [line.strip() for line in load_text_generator(txt_path)]


def write_list_to_txt(
    file_path: PathLike,
    data_list: List[Any],
    mode: str = "w",
    line_separator: str = "\n",
) -> None:
    """将列表内容写入文本文件。

    Args:
        file_path: 文件路径。
        data_list: 要写入的列表。
        mode: 'w' 覆盖，'a' 追加。
        line_separator: 行分隔符。
    """
    if not isinstance(data_list, list):
        raise TypeError("data_list must be a list")
    with open(file_path, mode, encoding="utf-8") as f:
        for item in data_list:
            f.write(f"{str(item)}{line_separator}")


def append_to_file(
    file_path: PathLike,
    content: str,
    encoding: str = "utf-8",
    add_newline: bool = True,
) -> None:
    """追加内容到文件末尾，文件不存在则自动创建。"""
    if add_newline:
        content += "\n"
    with open(file_path, "a", encoding=encoding) as f:
        f.write(content)


# ─────────────── JSON ───────────────


def load_json_from(file_path: PathLike) -> Union[List[Dict], Dict]:
    """从文件加载 JSON 数据（自动识别 list 或 dict）。"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_object_json_from(file_path: PathLike) -> Dict:
    """从文件加载 JSON 并确保返回 dict 类型。"""
    data = load_json_from(file_path)
    if isinstance(data, dict):
        return data
    raise ValueError(f"JSON at {file_path} is not a dict")


def load_list_json_from(file_path: PathLike) -> List[Dict]:
    """从文件加载 JSON 并确保返回 list 类型。"""
    data = load_json_from(file_path)
    if isinstance(data, list):
        return data
    raise ValueError(f"JSON at {file_path} is not a list")


def save_json_to(
    json_object: Union[Dict, List],
    folder_path: PathLike,
    file_name: str,
    *,
    indent: int = 4,
    ensure_ascii: bool = False,
) -> None:
    """将 JSON 数据保存到文件。

    Args:
        json_object: 要保存的数据。
        folder_path: 目标文件夹。
        file_name: 文件名。
        indent: 缩进空格数，默认 4。
        ensure_ascii: 是否转义非 ASCII 字符。
    """
    folder_path = Path(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)
    file_path = folder_path / file_name
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_object, f, ensure_ascii=ensure_ascii, indent=indent)


def read_jsonl(file_path: PathLike) -> List[Dict]:
    """读取 JSONL（JSON Lines）文件，返回 JSON 对象列表。"""
    with open(file_path, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]


def json_list_to_jsonl(json_list: List[Dict], jsonl_path: PathLike) -> None:
    """将 JSON 对象列表写入 JSONL 文件。"""
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for obj in json_list:
            json.dump(obj, f)
            f.write("\n")


# ─────────────── YAML ───────────────


def load_yaml_from(file_path: PathLike) -> Dict:
    """读取 YAML 文件并返回字典。"""
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# ─────────────── 文件 / 文件夹操作 ───────────────


def copy_file_to_folder(
    file_path: PathLike,
    folder_path: PathLike,
    target_name: Optional[str] = None,
) -> None:
    """复制文件到目标文件夹，文件夹不存在则创建。"""
    file_path = Path(file_path)
    folder_path = Path(folder_path)
    if file_path.is_dir():
        raise ValueError(f"{file_path} is not a file")
    folder_path.mkdir(parents=True, exist_ok=True)
    dest = folder_path / (target_name or file_path.name)
    shutil.copy(file_path, dest)
