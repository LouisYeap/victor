"""File I/O utilities — JSON / YAML / TXT / JSONL.

Example:
    >>> from victor.file import save_json_to, load_json_from
    >>> save_json_to({"name": "victor"}, "./data", "config.json", indent=2)
    >>> config = load_json_from("./data/config.json")
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Union

import yaml

from victor.types import PathLike

__all__ = (
    # text
    "load_text_from",
    "read_txt_to_list",
    "load_text_generator",
    "write_list_to_txt",
    "append_to_file",
    # JSON
    "load_json_from",
    "load_object_json_from",
    "load_list_json_from",
    "save_json_to",
    "read_jsonl",
    "json_list_to_jsonl",
    # YAML
    "load_yaml_from",
    # file operations
    "copy_file_to_folder",
)


# ─────────────── TXT ───────────────


def load_text_from(file_path: PathLike) -> str:
    """Read entire file contents as a single string."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_text_generator(file_path: PathLike):
    """Read a file line by line as a generator (memory-efficient for large files)."""
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


def read_txt_to_list(txt_path: PathLike) -> List[str]:
    """Read a text file, returning one stripped line per list element."""
    return [line.strip() for line in load_text_generator(txt_path)]


def write_list_to_txt(
    file_path: PathLike,
    data_list: List[Any],
    mode: str = "w",
    line_separator: str = "\n",
) -> None:
    """Write a list of items to a text file, one item per line.

    Args:
        file_path: Destination file path.
        data_list: List of items to write.
        mode: ``'w'`` to overwrite, ``'a'`` to append.
        line_separator: String appended after each item (default ``'\\n'``).
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
    """Append ``content`` to the end of a file. Creates the file if it does not exist.

    Args:
        file_path: Target file path.
        content: String content to append.
        encoding: File encoding (default ``utf-8``).
        add_newline: Whether to append a trailing newline (default ``True``).
    """
    if add_newline:
        content += "\n"
    with open(file_path, "a", encoding=encoding) as f:
        f.write(content)


# ─────────────── JSON ───────────────


def load_json_from(file_path: PathLike) -> Union[List[Dict], Dict]:
    """Load JSON from file; returns a dict or list depending on content."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_object_json_from(file_path: PathLike) -> Dict:
    """Load JSON from file, asserting that the root is a dict."""
    data = load_json_from(file_path)
    if isinstance(data, dict):
        return data
    raise ValueError(f"JSON at {file_path} is not a dict")


def load_list_json_from(file_path: PathLike) -> List[Dict]:
    """Load JSON from file, asserting that the root is a list."""
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
    """Save a JSON-serializable object to a file.

    Args:
        json_object: Python object to serialize.
        folder_path: Destination directory (created if missing).
        file_name: Output file name.
        indent: Spaces per indentation level (default 4).
        ensure_ascii: Escape non-ASCII characters (default ``False``).
    """
    folder_path = Path(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)
    file_path = folder_path / file_name
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_object, f, ensure_ascii=ensure_ascii, indent=indent)


def read_jsonl(file_path: PathLike) -> List[Dict]:
    """Read a JSONL (JSON Lines) file, returning a list of JSON objects."""
    with open(file_path, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]


def json_list_to_jsonl(json_list: List[Dict], jsonl_path: PathLike) -> None:
    """Write a list of JSON objects to a JSONL file (one object per line)."""
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for obj in json_list:
            json.dump(obj, f)
            f.write("\n")


# ─────────────── YAML ───────────────


def load_yaml_from(file_path: PathLike) -> Dict:
    """Load a YAML file and return its contents as a dict."""
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# ─────────────── File Operations ───────────────


def copy_file_to_folder(
    file_path: PathLike,
    folder_path: PathLike,
    target_name: str | None = None,
) -> None:
    """Copy a file into a destination folder, creating the folder if needed.

    Args:
        file_path: Source file path.
        folder_path: Destination folder.
        target_name: Optional rename on copy.
    """
    file_path = Path(file_path)
    folder_path = Path(folder_path)
    if file_path.is_dir():
        raise ValueError(f"{file_path} is not a file")
    folder_path.mkdir(parents=True, exist_ok=True)
    dest = folder_path / (target_name or file_path.name)
    shutil.copy(file_path, dest)
