import math
import os
from urllib.parse import urlparse


def get_obs_base_url(obs_url: str) -> str:
    """
    获取 OBS URL 的基础路径，即 `obs://bucket-name/`

    :param obs_url: 完整的 OBS URL,例如 "obs://vendor-sensetime/sensetime/250123/"
    :return: 解析后的基础 OBS 地址，例如 "obs://vendor-sensetime/"
    """
    parsed_url = urlparse(obs_url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}/"


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
