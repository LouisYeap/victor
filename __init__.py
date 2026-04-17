"""Victor — General-purpose Python utility library.

Provides multi-threaded/multi-process execution, file I/O, and common
development helpers for everyday coding tasks.
"""

from .accelerate_util import (
    thread_pool_executor,
    process_pool_executor,
    install_all_requirements,
    is_windows,
    get_absolute_path,
    clean_or_create_folder,
    clean_folder,
    clean_file,
    search,
    rsearch,
    list_folders_of_path,
    list_files_of_path,
    rlist_jsons_of_path,
    break_list,
    timing_decorator,
    fuzzy_get_value,
    fuzzy_get_keys,
)

from .file_utils import (
    load_text_from,
    read_txt_to_list,
    load_text_generator,
    load_json_from,
    load_object_json_from,
    load_list_json_from,
    save_json_to,
    copy_file_to_folder,
    load_yaml_from,
    write_list_to_txt,
    append_to_file,
    read_jsonl,
    json_list_to_jsonl,
)

from .command_utils import execute_command

from .dz_util import (
    get_obs_base_url,
    split_txt_file,
    split_datetime,
    split_list,
)

from .tool_types import IMAGE_FILE_EXTENSIONS, PathLike

__all__ = [
    # accelerate_util
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
    # file_utils
    "load_text_from",
    "read_txt_to_list",
    "load_text_generator",
    "load_json_from",
    "load_object_json_from",
    "load_list_json_from",
    "save_json_to",
    "copy_file_to_folder",
    "load_yaml_from",
    "write_list_to_txt",
    "append_to_file",
    "read_jsonl",
    "json_list_to_jsonl",
    # command_utils
    "execute_command",
    # dz_util
    "get_obs_base_url",
    "split_txt_file",
    "split_datetime",
    "split_list",
    # tool_types
    "IMAGE_FILE_EXTENSIONS",
    "PathLike",
]

__version__ = "1.0.0"
