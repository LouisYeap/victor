from pathlib import Path
import os
import platform
import shutil
import subprocess
from typing import List
from .tool_types import PathLike
import time


def install_all_requirements(root_dir="victor"):
    if not os.path.exists(root_dir):
        raise ValueError(f"root_dir {root_dir} not exists")

    requirement_files = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        requirement_files.extend(
            os.path.join(dirpath, file)
            for file in filenames
            if file.endswith("requirements.txt")
        )
    if not requirement_files:
        raise ValueError(f"no requirements.txt files found in {root_dir}")

    for req_file in requirement_files:
        print("installing requirements from", req_file)
        try:
            subprocess.run(["pip", "install", "-r", req_file], check=True)
            print(f"Successfully installed requirements from {req_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {req_file}: {e}")


def is_windows() -> bool:
    """
    判断当前操作系统是否为Windows。

    返回值:
        bool: 如果当前操作系统是Windows,则返回True;否则返回False。
    """
    return platform.system().startswith("Windows")


def get_absolute_path(relative_path: PathLike) -> Path:
    """
    获取文件或目录的绝对路径。在Windows系统上会自动处理长路径问题。

    Args:
        relative_path (PathLike): 相对路径或绝对路径字符串

    Returns:
        Path: 转换后的绝对路径对象
    """
    absolute_path = os.path.abspath(relative_path)

    if is_windows():
        absolute_path = f"\\\\?\\{absolute_path}"

    return Path(absolute_path)


def clean_or_create_folder(folder_path: PathLike):
    """
    清理已存在的文件夹或创建新文件夹。如果文件夹存在，会先删除再创建。

    Args:
        folder_path (PathLike): 要清理或创建的文件夹路径

    Returns:
        None
    """
    folder_path = Path(folder_path)
    if folder_path.exists():
        shutil.rmtree(folder_path)

    folder_path.mkdir(parents=True, exist_ok=True)


def clean_folder(folder_path: PathLike):
    """
    清理已存在的文件夹或创建新文件夹

    Args:
        folder_path (PathLike): 要清理或创建的文件夹路径

    Returns:
        None
    """
    folder_path = Path(folder_path)
    if folder_path.exists():
        shutil.rmtree(folder_path)


def clean_file(output_file: str):
    """
    清理临时文件
    """
    if Path(output_file).exists():
        Path(output_file).unlink()


def search(directory: PathLike, pattern: str) -> List[Path]:
    """
    在指定目录中搜索匹配指定模式的文件。

    Args:
        directory (PathLike): 要搜索的目录路径
        pattern (str): 搜索模式，支持通配符，如 "*.txt"

    Returns:
        List[Path]: 匹配文件的路径列表
    """
    return list(Path(directory).glob(pattern))


def rsearch(directory: PathLike, pattern: str) -> List[Path]:
    """
    递归地在指定目录及其子目录中搜索匹配指定模式的文件。

    Args:
        directory (PathLike): 要搜索的根目录路径
        pattern (str): 搜索模式，支持通配符，如 "*.txt"

    Returns:
        List[Path]: 匹配文件的路径列表
    """

    return list(Path(directory).rglob(pattern))


def list_folders_of_path(folder_path: PathLike):
    """
    获取指定路径下的所有文件夹。

    Args:
        folder_path (PathLike): 文件夹路径

    Returns:
        List[Path]: 文件夹路径列表
    """

    return [f for f in Path(folder_path).iterdir() if f.is_dir()]


def list_files_of_path(folder_path: PathLike):
    """
    获取指定路径下的所有文件。

    Args:
        folder_path (PathLike): 文件夹路径

    Returns:
        List[Path]: 文件路径列表
    """
    return [f for f in Path(folder_path).iterdir() if f.is_file()]


def rlist_jsons_of_path(folder_path: PathLike) -> List[Path]:
    """
    递归获取指定路径下的所有 JSON 文件（通过后缀名判断）。

    Args:
        folder_path (PathLike): 文件夹路径

    Returns:
        List[Path]: JSON 文件路径列表
    """
    return list(Path(folder_path).rglob("*.json"))


def break_list(lst: List, n: int) -> List[List]:
    """
    将一个列表分割成多个小列表，每个小列表包含最多 n 个元素。

    Args:
        lst (List): 需要分割的原始列表
        n (int): 每个子列表的最大元素数量

    Returns:
        List[List]: 一个嵌套列表，其中每个子列表包含 n 个或更少的元素
    """
    return [lst[i : i + n] for i in range(0, len(lst), n)]


def timing_decorator(func):
    """
    测试时间的装饰器
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)  # 执行被装饰的函数
        end_time = time.time()  # 记录结束时间
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")
        return result  # 返回函数的结果

    return wrapper


def fuzzy_get_value(data: dict, key_part: str):
    """模糊匹配 key,返回匹配的 value 列表"""
    return [v for k, v in data.items() if key_part in k]


def fuzzy_get_keys(data: dict, key_part: str):
    """模糊匹配 key,返回匹配的 key 列表"""
    return [k for k in data if key_part in k]
