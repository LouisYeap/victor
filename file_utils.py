import json
import shutil
from pathlib import Path
from typing import List, Optional, Union, Dict

import yaml

from .tool_types import PathLike


def load_text_from(file_path: PathLike) -> str:
    """从文件加载并返回文本数据"""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_json_from(file_path: PathLike) -> Union[List[Dict], Dict]:
    """从文件加载并返回 JSON 数据"""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_object_json_from(file_path: PathLike) -> Dict:
    """从文件加载并返回JSON 字典数据"""
    load_data = load_json_from(file_path)
    if isinstance(load_data, dict):
        return load_data
    raise ValueError("target json is not a object.")


def load_list_json_from(file_path: PathLike) -> Union[List[Dict], Dict]:
    """从文件加载并返回JSON 列表数据"""
    load_data = load_json_from(file_path)
    if isinstance(load_data, (list, dict)):
        return load_data
    raise ValueError("target json is not a object.")


def save_json_to(json_object: dict, folder_path: PathLike, file_name: str) -> None:
    """将 JSON 数据保存到文件"""
    folder_path = Path(folder_path)

    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)

    file_path = folder_path / file_name

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(json_object, file, ensure_ascii=False, indent=4)


def copy_file_to_folder(
    file_path: PathLike, folder_path: PathLike, target_name: Optional[str] = None
) -> None:
    """将文件复制到目标文件夹。如果文件夹不存在，创建该文件夹"""
    file_path = Path(file_path)
    folder_path = Path(folder_path)
    if file_path.is_dir():
        raise ValueError(f"{file_path} is not a file")

    folder_path.mkdir(parents=True, exist_ok=True)
    if target_name is not None:
        shutil.copy(file_path, folder_path / target_name)
    else:
        shutil.copy(file_path, folder_path)


def load_yaml_from(
    file_path: PathLike,
):  # -> Any | dict[Any, Any]:# -> Any | dict[Any, Any]:# -> Any | dict[Any, Any]:# -> Any | dict[Any, Any]:# -> Any | dict[Any, Any]:# -> Any | dict[Any, Any]:# -> Any | dict[Any, Any]:# -> Any | dict[Any, Any]:# -> Any | dict[Any, Any]:# -> Any | dict[Any, Any]:
    """
    这个函数用于读取指定路径的YAML文件，并将其内容解析为字典返回

    参数:
    file_path (str 或 Path): YAML文件在磁盘上的路径，可以是字符串类型或者pathlib.Path类型

    返回:
    dict: 解析后的YAML文件内容，以字典形式呈现，如果文件读取或解析出错，返回空字典
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}
