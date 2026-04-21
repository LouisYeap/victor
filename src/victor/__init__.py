"""Victor — General-purpose Python utility library.

Provides multi-threaded/multi-process execution, file I/O, and common
development helpers for everyday coding tasks.

Example:
    >>> from victor import thread_pool_executor, save_json_to, execute_command
    >>> thread_pool_executor(lambda x: x * x, [1, 2, 3, 4, 5])["results"]
    [1, 4, 9, 16, 25]
"""

from __future__ import annotations

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
    thread_pool_executor,
    timing_decorator,
)

from victor.command import execute_command

from victor.dz import (
    get_obs_base_url,
    split_datetime,
    split_list,
    split_txt_file,
)

from victor.file import (
    append_to_file,
    copy_file_to_folder,
    json_list_to_jsonl,
    load_json_from,
    load_list_json_from,
    load_object_json_from,
    load_text_from,
    load_text_generator,
    load_yaml_from,
    read_jsonl,
    read_txt_to_list,
    save_json_to,
    write_list_to_txt,
)

from victor.errors import (
    CommandFailedError,
    ErrorCode,
    FileNotFoundError,
    InvalidJSONError,
    InvalidTypeError,
    InvalidYAMLError,
    ParallelExecutionError,
    VictorError,
)

from victor.types import PathLike
from victor.version import __version__

__all__ = (
    # version
    "__version__",
    # errors
    "VictorError",
    "ErrorCode",
    "FileNotFoundError",
    "InvalidJSONError",
    "InvalidYAMLError",
    "InvalidTypeError",
    "CommandFailedError",
    "ParallelExecutionError",
    # types
    "PathLike",
    # accel — parallel execution
    "thread_pool_executor",
    "process_pool_executor",
    "install_all_requirements",
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
    "break_list",
    "timing_decorator",
    "fuzzy_get_value",
    "fuzzy_get_keys",
    # file
    "load_text_from",
    "read_txt_to_list",
    "load_text_generator",
    "write_list_to_txt",
    "append_to_file",
    "load_json_from",
    "load_object_json_from",
    "load_list_json_from",
    "save_json_to",
    "read_jsonl",
    "json_list_to_jsonl",
    "load_yaml_from",
    "copy_file_to_folder",
    # command
    "execute_command",
    # dz
    "get_obs_base_url",
    "split_txt_file",
    "split_datetime",
    "split_list",
)
