import json
import math
import os
from urllib.parse import urlparse
from . import accelerate_util
from . import command_utils
from . import file_utils
from xstorage_core import ObsPlugin, BaseObjectStoragePlugin

obs_plugin = ObsPlugin(
    "478SULZPVA3PMRBQEUHH",
    "exeTO3tK6lfz6pSjQhqO3tcPKBUmk84PImamRqTJ",
    "https://obs.cn-east-3.myhuaweicloud.com",
    "vendor-sensetime",
)


def get_obs_base_url(obs_url: str) -> str:
    """
    获取 OBS URL 的基础路径，即 `obs://bucket-name/`

    :param obs_url: 完整的 OBS URL,例如 "obs://vendor-sensetime/sensetime/250123/"
    :return: 解析后的基础 OBS 地址，例如 "obs://vendor-sensetime/"
    """
    parsed_url = urlparse(obs_url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}/"


def remove_clips(clips_obs_path: str, delete_clip_path: str):
    """
    删除指定的 OBS 路径下clip_name文件夹

    该函数根据指定的路径 `delete_clip_path` 中列出的剪辑标识符，从 OBS 路径 `clips_obs_path` 中删除对应的指定文件夹。函数会使用多线程并行执行删除操作，以提高删除效率。

    :param clips_obs_path: OBS 路径，包含待删除剪辑的存储路径。例如："obs://vendor-sensetime/sensetime/250123/"
    :param delete_clip_path: 存储要删除的剪辑标识符的文件路径。例如："clips_to_delete.txt",该文件应每行一个删除的clip_name行
    :return: 删除操作的执行结果，返回值为删除操作的执行结果
    """

    def delete_batch(paths):
        cmd = f"/obsutil/obsutil rm {' '.join(paths)} -r -f"
        # print("执行删除命令:", cmd)
        command_utils.execute_command(cmd)

    obs_origin_path = get_obs_base_url(clips_obs_path)

    with open(delete_clip_path, "r") as file:
        clip_set = {line.strip() for line in file}
    list_dir = obs_plugin.list_dir(
        clips_obs_path, BaseObjectStoragePlugin.VIEW_MODE_DIR, recursive=False
    )

    if not list_dir:
        print("该路径无数据")
        return
    delete_paths = [
        f"{obs_origin_path}{x}" for x in list_dir[1:] if x.split("/")[-2] in clip_set
    ]
    if not delete_paths:
        print("未找到匹配的文件夹")
        return
    print(f"执行删除 {len(delete_paths)} 个文件夹")

    result = accelerate_util.thread_pool_executor(
        delete_batch, delete_paths, pool_size=30
    )

    file_utils.append_to_file(
        "delete_result.txt", json.dumps(result, ensure_ascii=False)
    )


def split_txt_file(txt_path, split_count):
    """
    根据txt文档的行数拆分文件
    :param txt_path: txt文档路径
    :param split_count: 拆分的文件数量
    """
    # 读取原始 TXT 文件的所有内容
    with open(txt_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    total_lines = len(lines)
    if split_count > total_lines:
        print("拆分的文件数量大于总行数，每个文件最多包含一行")
        split_count = total_lines  # 防止创建过多文件

    # 计算每个文件应包含的平均行数
    lines_per_file = math.ceil(total_lines / split_count)  # 向上取整

    # 获取原始文件名（去掉扩展名）
    base_name, ext = os.path.splitext(txt_path)

    # 生成拆分后的多个文件
    for i in range(split_count):
        start_idx = i * lines_per_file
        end_idx = min((i + 1) * lines_per_file, total_lines)  # 确保不超出范围
        if start_idx >= total_lines:
            break  # 避免创建空文件

        part_file = f"{base_name}_{i + 1}{ext}"  # 生成文件名，如 `file_1.txt`
        with open(part_file, "w", encoding="utf-8") as part:
            part.writelines(lines[start_idx:end_idx])

        print(f"生成文件: {part_file}, 包含 {end_idx - start_idx} 行")
