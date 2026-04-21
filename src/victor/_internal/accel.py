"""Internal parallel execution utilities.

This module is private. Use the public wrappers in ``victor`` instead.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from multiprocessing import Pool
from pathlib import Path
from typing import Any, Callable

import tqdm

from victor._internal.typing import MISSING
from victor.types import PathLike


def thread_pool_executor(
    func: Callable[..., Any],
    tasks: list,
    *,
    pool_size: int = 60,
    desc: str = "Processing...",
    timeout: float | None = None,
) -> dict[str, list[Any]]:
    """General-purpose multi-threaded task executor with tqdm progress bar.

    Args:
        func: Callable to apply to each task.
        tasks: List of tasks (single values or tuples passed as *args).
        pool_size: Maximum concurrent threads (default 60).
        desc: Progress bar description.
        timeout: Per-task timeout in seconds (default None = no limit).

    Returns:
        dict with ``results`` (list of return values) and ``errors`` (list of error messages).
    """
    results: list[Any] = []
    error_msgs: list[str] = []

    with tqdm.tqdm(total=len(tasks), desc=desc, leave=True) as pbar:
        with ThreadPoolExecutor(max_workers=pool_size) as executor:
            future_tasks: list[Future[Any]] = [
                executor.submit(
                    func, *task if isinstance(task, (tuple, list)) else (task,)
                )
                for task in tasks
            ]
            for future in as_completed(future_tasks):
                try:
                    result = future.result(timeout=timeout)
                    if result is not None:
                        results.append(result)
                except Exception as e:
                    error_msgs.append(
                        f"Task error: {type(e).__name__}: {e}\n{traceback.format_exc()}"
                    )
                pbar.update(1)

    return {"results": results, "errors": error_msgs}


def process_pool_executor(
    func: Callable[..., Any],
    tasks: list,
    *,
    pool_size: int | None = None,
    desc: str = "Processing...",
    timeout: float | None = None,
) -> dict[str, list[Any]]:
    """Parallel task execution using ``multiprocessing.Pool`` with tqdm.

    Args:
        func: Callable to apply to each task.
        tasks: List of tasks (single values or tuples passed as *args).
        pool_size: Number of worker processes (default = CPU count).
        desc: Progress bar description.
        timeout: Per-task timeout in seconds (default None = no limit).

    Returns:
        dict with ``results`` (list of return values) and ``errors`` (list of error messages).
    """
    if pool_size is None:
        pool_size = os.cpu_count() or 8

    results: list[Any] = []
    error_msgs: list[str] = []

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
                    results.append(ar.get(timeout=timeout))
                except Exception as e:
                    error_msgs.append(
                        f"Task error: {type(e).__name__}: {e}\n{traceback.format_exc()}"
                    )
                pbar.update(1)

    return {"results": results, "errors": error_msgs}


def install_all_requirements(root_dir: PathLike = ".") -> None:
    """Recursively install all ``requirements.txt`` files under a directory."""
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
        print(f"  OK  {req_file}")


def is_windows() -> bool:
    """Return ``True`` if the current OS is Windows."""
    return platform.system().startswith("Windows")


def get_absolute_path(relative_path: PathLike) -> Path:
    """Convert a relative path to absolute; handles Windows long-path prefix."""
    absolute_path = os.path.abspath(relative_path)
    if is_windows():
        absolute_path = f"\\\\?\\{absolute_path}"
    return Path(absolute_path)


def clean_or_create_folder(folder_path: PathLike) -> None:
    """Delete the folder if it exists, then create it fresh."""
    folder_path = Path(folder_path)
    if folder_path.exists():
        shutil.rmtree(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)


def clean_folder(folder_path: PathLike) -> bool:
    """Delete a folder and all its contents (if it exists).

    Returns:
        True if the folder existed and was deleted, False otherwise.
    """
    folder_path = Path(folder_path)
    if folder_path.exists():
        shutil.rmtree(folder_path)
        return True
    return False


def clean_file(output_file: PathLike) -> bool:
    """Delete a file (if it exists).

    Returns:
        True if the file existed and was deleted, False otherwise.
    """
    p = Path(output_file)
    if p.exists():
        p.unlink()
        return True
    return False


def search(directory: PathLike, pattern: str) -> list[Path]:
    """Search for files matching ``pattern`` in ``directory`` (non-recursive)."""
    return list(Path(directory).glob(pattern))


def rsearch(directory: PathLike, pattern: str) -> list[Path]:
    """Recursively search for files matching ``pattern`` under ``directory``."""
    return list(Path(directory).rglob(pattern))


def list_folders_of_path(folder_path: PathLike) -> list[Path]:
    """Return all subfolders under ``folder_path``."""
    return [f for f in Path(folder_path).iterdir() if f.is_dir()]


def list_files_of_path(folder_path: PathLike) -> list[Path]:
    """Return all files under ``folder_path``."""
    return [f for f in Path(folder_path).iterdir() if f.is_file()]


def rlist_jsons_of_path(folder_path: PathLike) -> list[Path]:
    """Recursively find all JSON files under ``folder_path``."""
    return list(Path(folder_path).rglob("*.json"))


def break_list(lst: list[T], n: int) -> list[list[T]]:
    """Split ``lst`` into chunks of at most ``n`` elements each."""
    return [lst[i : i + n] for i in range(0, len(lst), n)]


def timing_decorator(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator that prints ``func``'s execution time to stdout."""

    def wrapper(*args, **kwargs) -> T:
        start = time.time()
        result = func(*args, **kwargs)
        print(f"[{func.__name__}] executed in {time.time() - start:.4f}s")
        return result

    return wrapper


def fuzzy_get_value(data: dict, key_part: str) -> list[Any]:
    """Return all values whose keys contain ``key_part``."""
    return [v for k, v in data.items() if key_part in k]


def fuzzy_get_keys(data: dict, key_part: str) -> list[str]:
    """Return all keys that contain ``key_part``."""
    return [k for k in data if key_part in k]
