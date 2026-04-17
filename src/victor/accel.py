"""Thread / process pool parallel task execution.

Example:
    >>> from victor.accel import thread_pool_executor
    >>> def square(x): return x * x
    >>> thread_pool_executor(square, [1, 2, 3, 4, 5])["results"]
    [1, 4, 9, 16, 25]
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, TypeVar, Union, Tuple

from victor._internal.accel import (
    break_list,
    clean_file,
    clean_folder,
    clean_or_create_folder,
    fuzzy_get_keys,
    fuzzy_get_value,
    get_absolute_path,
    install_all_requirements,
    is_windows,
    list_files_of_path,
    list_folders_of_path,
    process_pool_executor,
    rlist_jsons_of_path,
    rsearch,
    search,
    timing_decorator,
    thread_pool_executor,
)
from victor.types import PathLike

__all__ = (
    # executor
    "thread_pool_executor",
    "process_pool_executor",
    "install_all_requirements",
    # path utilities
    "is_windows",
    "get_absolute_path",
    "clean_or_create_folder",
    "clean_folder",
    "clean_file",
    "search",
    "rsearch",
    "list_folders_of_path",
    "list_files_of_path",
    "rlist_jsons_of_path",
    # list utilities
    "break_list",
    # decorators
    "timing_decorator",
    # dict utilities
    "fuzzy_get_value",
    "fuzzy_get_keys",
)

T = TypeVar("T")
