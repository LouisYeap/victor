import json
import shutil
from pathlib import Path
from typing import List, Optional, Union, Dict

import yaml
import aiofiles

from .tool_types import PathLike


async def load_text_from_async(file_path: PathLike) -> str:
    """从文件加载并返回文本数据 (异步)"""
    async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
        return await file.read()


async def load_json_from_async(file_path: PathLike) -> Union[List[Dict], Dict]:
    """从文件加载并返回 JSON 数据 (异步)"""
    async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
        content = await file.read()
        return json.loads(content)


async def load_object_json_from_async(file_path: PathLike) -> Dict:
    """从文件加载并返回 JSON 字典数据 (异步)"""
    load_data = await load_json_from_async(file_path)
    if isinstance(load_data, dict):
        return load_data
    raise ValueError("target json is not a object.")


async def load_list_json_from_async(file_path: PathLike) -> Union[List[Dict], Dict]:
    """从文件加载并返回 JSON 列表数据 (异步)"""
    load_data = await load_json_from_async(file_path)
    if isinstance(load_data, (list, dict)):
        return load_data
    raise ValueError("target json is not a object.")


async def save_json_to_async(
    json_object: dict, folder_path: PathLike, file_name: str
) -> None:
    """将 JSON 数据保存到文件 (异步)"""
    folder_path = Path(folder_path)

    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)

    file_path = folder_path / file_name

    async with aiofiles.open(file_path, "w", encoding="utf-8") as file:
        await file.write(json.dumps(json_object, ensure_ascii=False, indent=4))


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


async def load_yaml_from_async(file_path: PathLike) -> Dict:
    """
    从文件加载并返回 YAML 数据 (异步)

    参数:
    file_path (str 或 Path): YAML 文件在磁盘上的路径，可以是字符串类型或者 pathlib.Path 类型

    返回:
    dict: 解析后的 YAML 文件内容，以字典形式呈现
    """
    async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
        content = await file.read()
        return yaml.safe_load(content) or {}
