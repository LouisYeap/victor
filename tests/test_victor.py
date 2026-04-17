"""Victor 工具库测试"""

import json
import os
import tempfile
from pathlib import Path

import pytest

# ─────────────── 辅助 ───────────────

TMP = tempfile.mkdtemp()


def test_load_and_save_json(tmp_path):
    from victor import save_json_to, load_json_from

    data = {"name": "victor", "version": "1.0.0", "features": ["fast", "simple"]}
    save_json_to(data, tmp_path, "test.json")
    loaded = load_json_from(tmp_path / "test.json")
    assert loaded == data


def test_save_json_indent(tmp_path):
    from victor import save_json_to

    save_json_to({"a": 1}, tmp_path, "indent.json", indent=2)
    content = (tmp_path / "indent.json").read_text()
    # 缩进为2空格
    assert "  " in content and '"a"' in content


def test_save_json_ensure_ascii(tmp_path):
    from victor import save_json_to, load_json_from

    save_json_to({"name": "你好"}, tmp_path, "unicode.json", ensure_ascii=True)
    raw = (tmp_path / "unicode.json").read_text()
    assert "你好" not in raw  # 应被转义
    loaded = load_json_from(tmp_path / "unicode.json")
    assert loaded["name"] == "你好"


def test_load_object_json_from_valid(tmp_path):
    from victor import save_json_to, load_object_json_from

    save_json_to({"key": "value"}, tmp_path, "obj.json")
    assert load_object_json_from(tmp_path / "obj.json") == {"key": "value"}


def test_load_object_json_from_invalid(tmp_path):
    from victor import load_object_json_from

    path = tmp_path / "list.json"
    path.write_text("[1, 2, 3]", encoding="utf-8")
    with pytest.raises(ValueError):
        load_object_json_from(path)


def test_load_list_json_from_valid(tmp_path):
    from victor import save_json_to, load_list_json_from

    save_json_to([1, 2, 3], tmp_path, "list.json")
    assert load_list_json_from(tmp_path / "list.json") == [1, 2, 3]


def test_load_list_json_from_invalid(tmp_path):
    from victor import load_list_json_from

    path = tmp_path / "dict.json"
    path.write_text('{"key": "value"}', encoding="utf-8")
    with pytest.raises(ValueError):
        load_list_json_from(path)


def test_read_write_txt(tmp_path):
    from victor import write_list_to_txt, read_txt_to_list

    tmp = tmp_path / "lines.txt"
    write_list_to_txt(tmp, ["hello", "world", "victor"])
    lines = read_txt_to_list(tmp)
    assert lines == ["hello", "world", "victor"]


def test_write_txt_append_mode(tmp_path):
    from victor import write_list_to_txt

    tmp = tmp_path / "append.txt"
    write_list_to_txt(tmp, ["first"])
    write_list_to_txt(tmp, ["second"], mode="a")
    content = tmp.read_text(encoding="utf-8")
    assert "first" in content and "second" in content


def test_write_list_to_txt_type_error():
    from victor import write_list_to_txt

    with pytest.raises(TypeError):
        write_list_to_txt("/tmp/dummy.txt", "not a list")


def test_append_to_file(tmp_path):
    from victor import append_to_file, load_text_from

    p = tmp_path / "append.txt"
    append_to_file(p, "line1")
    append_to_file(p, "line2", add_newline=False)
    # add_newline=False 时最后无换行符
    assert load_text_from(p) == "line1\nline2"


def test_jsonl_roundtrip(tmp_path):
    from victor import json_list_to_jsonl, read_jsonl

    data = [{"id": 1}, {"id": 2}, {"id": 3}]
    path = tmp_path / "test.jsonl"
    json_list_to_jsonl(data, path)
    loaded = read_jsonl(path)
    assert loaded == data


def test_yaml_roundtrip(tmp_path):
    from victor import load_yaml_from

    path = tmp_path / "config.yaml"
    content = "server:\n  host: localhost\n  port: 8080\n"
    path.write_text(content, encoding="utf-8")
    data = load_yaml_from(path)
    assert data["server"]["host"] == "localhost"
    assert data["server"]["port"] == 8080


def test_load_yaml_from_empty(tmp_path):
    from victor import load_yaml_from

    path = tmp_path / "empty.yaml"
    path.write_text("", encoding="utf-8")
    assert load_yaml_from(path) == {}


# ─────────────── accelerate_util ───────────────

def _cube(x):
    return x ** 3


def test_thread_pool_executor():
    from victor import thread_pool_executor

    def square(x):
        return x * x

    result = thread_pool_executor(square, [1, 2, 3, 4, 5], pool_size=4)
    assert sorted(result["results"]) == [1, 4, 9, 16, 25]
    assert result["errors"] == []


def test_thread_pool_executor_with_errors():
    from victor import thread_pool_executor

    def fail(x):
        raise ValueError("test error")

    result = thread_pool_executor(fail, [1, 2, 3], pool_size=2)
    assert len(result["results"]) == 0
    assert len(result["errors"]) == 3


def test_process_pool_executor():
    from victor import process_pool_executor

    result = process_pool_executor(_cube, [1, 2, 3], pool_size=2)
    assert sorted(result["results"]) == [1, 8, 27]


def test_break_list():
    from victor import break_list

    assert break_list([1, 2, 3, 4, 5, 6, 7], 3) == [[1, 2, 3], [4, 5, 6], [7]]


def test_fuzzy_get_value():
    from victor import fuzzy_get_value

    data = {"server_host": "localhost", "server_port": 8080, "client_host": "remote"}
    assert set(fuzzy_get_value(data, "server")) == {"localhost", 8080}


def test_fuzzy_get_keys():
    from victor import fuzzy_get_keys

    data = {"server_host": "localhost", "server_port": 8080, "client_host": "remote"}
    assert set(fuzzy_get_keys(data, "server")) == {"server_host", "server_port"}


def test_is_windows():
    from victor import is_windows

    result = is_windows()
    assert isinstance(result, bool)


def test_clean_or_create_folder(tmp_path):
    from victor import clean_or_create_folder

    sub = tmp_path / "sub"
    clean_or_create_folder(sub)
    assert sub.exists() and sub.is_dir()

    # 再次调用：已有目录应被删除重建
    (sub / "temp.txt").write_text("hello", encoding="utf-8")
    clean_or_create_folder(sub)
    assert sub.exists()
    assert not (sub / "temp.txt").exists()


def test_clean_folder(tmp_path):
    from victor import clean_folder

    sub = tmp_path / "cleanable"
    sub.mkdir()
    (sub / "file.txt").write_text("hello", encoding="utf-8")
    clean_folder(sub)
    assert not sub.exists()


def test_clean_file(tmp_path):
    from victor import clean_file

    f = tmp_path / "to_delete.txt"
    f.write_text("hello", encoding="utf-8")
    clean_file(f)
    assert not f.exists()


def test_search(tmp_path):
    from victor import search

    (tmp_path / "a.txt").touch()
    (tmp_path / "b.txt").touch()
    (tmp_path / "c.json").touch()

    assert len(search(tmp_path, "*.txt")) == 2
    assert len(search(tmp_path, "*.json")) == 1


def test_rsearch(tmp_path):
    from victor import rsearch

    sub = tmp_path / "sub"
    sub.mkdir()
    (tmp_path / "root.txt").touch()
    (sub / "nested.txt").touch()

    assert len(rsearch(tmp_path, "*.txt")) == 2


def test_list_folders_of_path(tmp_path):
    from victor import list_folders_of_path

    (tmp_path / "folder1").mkdir()
    (tmp_path / "folder2").mkdir()
    (tmp_path / "file.txt").touch()

    dirs = list_folders_of_path(tmp_path)
    assert len(dirs) == 2


def test_list_files_of_path(tmp_path):
    from victor import list_files_of_path

    (tmp_path / "a.txt").touch()
    (tmp_path / "b.txt").touch()
    (tmp_path / "folder").mkdir()

    files = list_files_of_path(tmp_path)
    assert len(files) == 2


def test_timing_decorator(capsys):
    from victor import timing_decorator

    @timing_decorator
    def quick():
        return 42

    result = quick()
    assert result == 42


# ─────────────── dz_util ───────────────

def test_split_list():
    from victor import split_list

    parts = split_list([1, 2, 3, 4, 5, 6, 7], 3)
    assert len(parts) == 3
    assert sum(len(p) for p in parts) == 7


def test_split_list_even():
    from victor import split_list

    parts = split_list([1, 2, 3, 4], 2)
    assert parts == [[1, 2], [3, 4]]


def test_split_txt_file(tmp_path):
    from victor import split_txt_file

    f = tmp_path / "source.txt"
    f.write_text("\n".join(str(i) for i in range(10)), encoding="utf-8")

    split_txt_file(str(f), 3)

    files = sorted(tmp_path.glob("source_*.txt"))
    assert len(files) == 3
    # 总行数应为 10（9个数字 + 空行尾）
    total_lines = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in files)
    assert total_lines == 10


def test_get_obs_base_url():
    from victor import get_obs_base_url

    assert get_obs_base_url("obs://bucket-name/path/to/file") == "obs://bucket-name/"
    assert get_obs_base_url("obs://my-bucket/a/b/c") == "obs://my-bucket/"


# ─────────────── command_utils ───────────────

def test_execute_command_success():
    from victor import execute_command

    result = execute_command("echo hello", switch=True)
    assert result == "hello"


def test_execute_command_failure():
    from victor import execute_command

    # 不存在的命令应该返回命令字符串（失败标志）
    ret = execute_command("exit 1", switch=False)
    # 命令失败时返回命令字符串作为失败标志
    assert ret == "exit 1"
