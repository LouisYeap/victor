"""并行任务处理工具（线程池 / 进程池）"""

import os
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from multiprocessing import Pool
from pathlib import Path
from typing import Any, Callable, Dict, List, TypeVar, Union, Tuple

import tqdm

T = TypeVar("T")


def thread_pool_executor(
    func: Callable[..., Any],
    tasks: List[Union[Any, Tuple[Any, ...]]],
    pool_size: int = 60,
    desc: str = "线程池处理中...",
) -> Dict[str, List[Any]]:
    """通用多线程任务处理。

    Args:
        func: 执行任务的函数，接受一个或多个参数。
        tasks: 任务列表，每个任务可以是单参数或元组/列表（表示多参数）。
        pool_size: 线程池大小，默认 60。
        desc: 进度条描述。

    Returns:
        包含结果和错误信息的字典 ``{'results': [], 'errors': []}``。

    示例:
        >>> def square(x): return x * x
        >>> thread_pool_executor(square, [1, 2, 3, 4, 5])['results']
        [1, 4, 9, 16, 25]
    """
    results, error_msgs = [], []

    with tqdm.tqdm(total=len(tasks), desc=desc, leave=True) as pbar:
        with ThreadPoolExecutor(max_workers=pool_size) as executor:
            future_tasks: List[Future[Any]] = [
                executor.submit(func, *task if isinstance(task, (tuple, list)) else (task,))
                for task in tasks
            ]
            for future in as_completed(future_tasks):
                try:
                    result = future.result()
                    if result is not None:
                        results.append(result)
                except Exception as e:
                    error_msgs.append(
                        f"任务出错: {type(e).__name__}: {e}\n{traceback.format_exc()}"
                    )
                pbar.update(1)

    return {"results": results, "errors": error_msgs}


def process_pool_executor(
    func: Callable[..., Any],
    tasks: List[Union[Any, Tuple[Any, ...]]],
    pool_size: int = None,
    desc: str = "进程池处理中...",
) -> Dict[str, List[Any]]:
    """使用 ``multiprocessing.Pool`` 并行执行任务，带 tqdm 进度条。

    Args:
        func: 需要并行执行的函数。
        tasks: 任务列表，每个任务可以是单参数或元组/列表（多参数）。
        pool_size: 进程池大小，默认为 CPU 核心数。
        desc: 进度条描述。

    Returns:
        包含结果和错误信息的字典 ``{'results': [], 'errors': []}``。

    示例:
        >>> def square(x): return x * x
        >>> process_pool_executor(square, [1, 2, 3, 4, 5])['results']
        [1, 4, 9, 16, 25]
    """
    if pool_size is None:
        pool_size = os.cpu_count() or 8

    results, error_msgs = [], []

    with Pool(processes=pool_size) as pool:
        async_results = [
            pool.apply_async(
                func, args=task if isinstance(task, (tuple, list)) else (task,)
            )
            for task in tasks
        ]
        with tqdm.tqdm(total=len(async_results), desc=desc, unit="task", leave=True) as pbar:
            for ar in async_results:
                try:
                    results.append(ar.get())
                except Exception as e:
                    error_msgs.append(
                        f"任务出错: {type(e).__name__}: {e}\n{traceback.format_exc()}"
                    )
                pbar.update(1)

    return {"results": results, "errors": error_msgs}


# ─────────────── 以下为路径 / 文件夹操作工具 ───────────────
#（保留在本文件以维持向后兼容，建议逐步迁移到 file_utils）

import platform
import shutil
import subprocess
from .tool_types import PathLike


def install_all_requirements(root_dir: PathLike = "."):
    """递归安装目录下所有 requirements.txt 文件。

    Args:
        root_dir: 搜索根目录。
    """
    req_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        req_files.extend(
            os.path.join(dirpath, f) for f in filenames if f == "requirements.txt"
        )
    if not req_files:
        raise ValueError(f"no requirements.txt found under {root_dir}")

    for req_file in req_files:
        print(f"Installing from {req_file} ...")
        subprocess.run(["pip", "install", "-r", req_file], check=True)
        print(f"✓ {req_file}")


def is_windows() -> bool:
    """判断当前系统是否为 Windows。"""
    return platform.system().startswith("Windows")


def get_absolute_path(relative_path: PathLike) -> Path:
    """将相对路径转换为绝对路径，Windows 下自动处理长路径。"""
    absolute_path = os.path.abspath(relative_path)
    if is_windows():
        absolute_path = f"\\\\?\\{absolute_path}"
    return Path(absolute_path)


def clean_or_create_folder(folder_path: PathLike) -> None:
    """如果文件夹存在则删除重建，否则直接创建。"""
    folder_path = Path(folder_path)
    if folder_path.exists():
        shutil.rmtree(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)


def clean_folder(folder_path: PathLike) -> None:
    """删除文件夹（如果存在）。"""
    folder_path = Path(folder_path)
    if folder_path.exists():
        shutil.rmtree(folder_path)


def clean_file(output_file: PathLike) -> None:
    """删除文件（如果存在）。"""
    p = Path(output_file)
    if p.exists():
        p.unlink()


def search(directory: PathLike, pattern: str) -> List[Path]:
    """在目录中搜索匹配 pattern 的文件（非递归）。"""
    return list(Path(directory).glob(pattern))


def rsearch(directory: PathLike, pattern: str) -> List[Path]:
    """在目录及其子目录中递归搜索匹配 pattern 的文件。"""
    return list(Path(directory).rglob(pattern))


def list_folders_of_path(folder_path: PathLike) -> List[Path]:
    """返回指定路径下的所有子文件夹。"""
    return [f for f in Path(folder_path).iterdir() if f.is_dir()]


def list_files_of_path(folder_path: PathLike) -> List[Path]:
    """返回指定路径下的所有文件。"""
    return [f for f in Path(folder_path).iterdir() if f.is_file()]


def rlist_jsons_of_path(folder_path: PathLike) -> List[Path]:
    """递归获取指定路径下所有 JSON 文件。"""
    return list(Path(folder_path).rglob("*.json"))


def break_list(lst: List[T], n: int) -> List[List[T]]:
    """将列表均分成每份最多 n 个元素。"""
    return [lst[i : i + n] for i in range(0, len(lst), n)]


def timing_decorator(func: Callable[..., T]) -> Callable[..., T]:
    """打印函数执行耗时的装饰器。"""
    def wrapper(*args, **kwargs) -> T:
        start = time.time()
        result = func(*args, **kwargs)
        print(f"[{func.__name__}] executed in {time.time() - start:.4f}s")
        return result
    return wrapper


def fuzzy_get_value(data: dict, key_part: str) -> List[Any]:
    """模糊匹配 key，返回对应的 value 列表。"""
    return [v for k, v in data.items() if key_part in k]


def fuzzy_get_keys(data: dict, key_part: str) -> List[str]:
    """模糊匹配 key，返回匹配的 key 列表。"""
    return [k for k in data if key_part in k]
