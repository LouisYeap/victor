import datetime
from pathlib import Path
import os
import platform
import shutil
import subprocess
from typing import List
from .tool_types import PathLike, IMAGE_FILE_EXTENSIONS
import time


def handle_errors(errors: list, output_name: str) -> None:
    """
    将错误信息写入文件。

    参数:
        errors (list): 错误信息的列表。
        script_name (str): 错误文件的名称（通常为脚本名加 `_error.txt`）。
    """
    with open(output_name, "w") as file:
        file.write("\n".join(errors))
        file.flush()
        os.fsync(file.fileno())
    print(f"所有错误信息已保存到: {output_name}")


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
        bool: 如果当前操作系统是Windows，则返回True；否则返回False。
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


def is_image_file(file_path: PathLike) -> bool:
    """
    检查给定路径的文件，通过文件后缀判断是否是图片文件。
    如果需要更加准确的判断请用 `guess_image`。

    Args:
        file_path (Path): 文件路径对象

    Returns:
        bool: 如果是图片文件，返回 True；否则返回 False。
    """
    file_path = Path(file_path)
    # 检查路径是否是文件并且扩展名是否在 IMAGE_FILE_EXTENSIONS 中
    return (
        file_path.is_file()
        and file_path.suffix.lower().split(".")[-1] in IMAGE_FILE_EXTENSIONS
    )


def list_images_of_path(folder_path: PathLike):
    """
    获取指定路径下的所有图片（通过后缀名判断）。

    Args:
        folder_path (PathLike): 文件夹路径

    Returns:
        List[Path]: 图片路径列表
    """
    return [
        f
        for f in Path(folder_path).iterdir()
        if f.suffix.lower() in IMAGE_FILE_EXTENSIONS
    ]


def rlist_images_of_path(folder_path: PathLike) -> List[Path]:
    """
    递归获取指定路径下的所有图片（通过后缀名判断）。

    Args:
        folder_path (PathLike): 文件夹路径

    Returns:
        List[Path]: 图片路径列表
    """
    return [f for f in Path(folder_path).rglob("*") if is_image_file(f)]


def rlist_jsons_of_path(folder_path: PathLike) -> List[Path]:
    """
    递归获取指定路径下的所有 JSON 文件（通过后缀名判断）。

    Args:
        folder_path (PathLike): 文件夹路径

    Returns:
        List[Path]: JSON 文件路径列表
    """
    return list(Path(folder_path).rglob("*.json"))


def rlist_pcd_of_path(folder_path: PathLike) -> List[Path]:
    """
    递归获取指定路径下的所有 pcd 文件（通过后缀名判断）。

    Args:
        folder_path (PathLike): 文件夹路径

    Returns:
        List[Path]: JSON 文件路径列表
    """
    return list(Path(folder_path).rglob("*.pcd"))


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


def remove_duplicates(lst: list) -> list:
    """
    从列表中移除重复元素，并返回一个不含重复元素的新列表。

    Args:
        lst: 一个可能包含重复元素的列表

    Returns:
        一个新列表，包含原列表中所有唯一元素，会保证原有顺序
    """
    seen = set()
    return [x for x in lst if x not in seen and not seen.add(x)]


def get_current_datetime(format_str: str = "%Y-%m-%d-%H-%M-%S") -> str:
    """
    根据指定的格式，返回现当前的日期时间，默认格式是 %Y-%m-%d-%H-%M-%S, 2024-12-12-20-30-45

    参数：
        format_str (str): 格式化字符串

    返回：
        str: 格式化后的日期时间
    """
    return datetime.datetime.now().strftime(format_str)


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)  # 执行被装饰的函数
        end_time = time.time()  # 记录结束时间
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")
        return result  # 返回函数的结果

    return wrapper
