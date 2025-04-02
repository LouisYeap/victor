from datetime import datetime, timedelta
from itertools import islice
import math
import os
from typing import List, Tuple
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


def split_datetime(
    start_date: str, end_date: str, parallelism: int
) -> List[List[Tuple[str, str]]]:
    """
    日期拆分
    例子:"20250101" "20250201"
    """
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    total_days = (end_dt - start_dt).days
    if total_days < parallelism:
        raise ValueError("parallelism 不能大于时间范围内的天数")

    chunk_size = total_days // parallelism
    remainder = total_days % parallelism

    date_splits = []
    current_date = start_dt

    for i in range(parallelism):
        sub_chunk_size = chunk_size + (1 if i < remainder else 0)
        sub_list = []

        for _ in range(sub_chunk_size):
            next_date = current_date + timedelta(days=1)
            if next_date > end_dt:
                break
            sub_list.append(
                (current_date.strftime("%Y-%m-%d"), next_date.strftime("%Y-%m-%d"))
            )
            current_date = next_date

        date_splits.append(sub_list)

        if current_date >= end_dt:
            break

    return date_splits


def split_list(lst, n):
    """
    将列表 lst 拆分为 n 份，每份大小尽量均匀。

    :param lst: 需要拆分的列表
    :param n: 需要拆分的部分数
    :return: 拆分后的列表
    """
    avg, extra = divmod(len(lst), n)
    iter_lst = iter(lst)
    return [list(islice(iter_lst, avg + (i < extra))) for i in range(n)]


