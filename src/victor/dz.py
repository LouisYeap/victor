"""Date-range splitting, OBS URL parsing, and other domain utilities.

Example:
    >>> from victor.dz import split_list, get_obs_base_url
    >>> split_list([1, 2, 3, 4, 5, 6, 7], 3)
    [[1, 2, 3], [4, 5, 6], [7]]
    >>> get_obs_base_url("obs://my-bucket/path/to/file")
    'obs://my-bucket/'
"""

from __future__ import annotations

import math
import os
from datetime import datetime, timedelta
from itertools import islice
from typing import List, Tuple, TypeVar
from urllib.parse import urlparse

__all__ = (
    "get_obs_base_url",
    "split_txt_file",
    "split_datetime",
    "split_list",
)

T = TypeVar("T")


def get_obs_base_url(obs_url: str) -> str:
    """Extract the bucket base path ``obs://bucket-name/`` from a full OBS URL.

    Example:
        >>> get_obs_base_url("obs://my-bucket/path/to/file")
        'obs://my-bucket/'
    """
    parsed_url = urlparse(obs_url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}/"


def split_txt_file(txt_path: str, split_count: int) -> None:
    """Split a text file into ``split_count`` roughly equal output files.

    Each output file is named ``{basename}_{i}{ext}`` (1-indexed).

    Args:
        txt_path: Path to the source text file.
        split_count: Number of output files to produce.
    """
    with open(txt_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    total_lines = len(lines)
    if split_count > total_lines:
        print("split_count exceeds total lines; capping to total_lines")
        split_count = total_lines

    lines_per_file = math.ceil(total_lines / split_count)
    base_name, ext = os.path.splitext(txt_path)

    for i in range(split_count):
        start_idx = i * lines_per_file
        end_idx = min((i + 1) * lines_per_file, total_lines)
        if start_idx >= total_lines:
            break  # avoid empty files

        part_file = f"{base_name}_{i + 1}{ext}"
        with open(part_file, "w", encoding="utf-8") as part:
            part.writelines(lines[start_idx:end_idx])

        print(f"Created {part_file} with {end_idx - start_idx} lines")


def split_datetime(
    start_date: str,
    end_date: str,
    parallelism: int,
) -> List[List[Tuple[str, str]]]:
    """Split a date range into ``parallelism`` roughly equal periods.

    Each period is returned as a list of ``(start, end)`` date-str tuples.

    Args:
        start_date: Start date in ``YYYY-MM-DD`` format.
        end_date: End date in ``YYYY-MM-DD`` format.
        parallelism: Number of chunks to produce.

    Returns:
        A list of chunks, each a list of ``(date, next_date)`` tuples.

    Example:
        >>> split_datetime("2025-01-01", "2025-01-10", 3)
    """
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    total_days = (end_dt - start_dt).days
    if total_days < parallelism:
        raise ValueError("parallelism cannot exceed total days in range")

    chunk_size = total_days // parallelism
    remainder = total_days % parallelism

    date_splits: List[List[Tuple[str, str]]] = []
    current_date = start_dt

    for i in range(parallelism):
        days_in_chunk = chunk_size + (1 if i < remainder else 0)
        sub_list: List[Tuple[str, str]] = []

        for _ in range(days_in_chunk):
            next_date = current_date + timedelta(days=1)
            sub_list.append(
                (current_date.strftime("%Y-%m-%d"), next_date.strftime("%Y-%m-%d"))
            )
            current_date = next_date

        date_splits.append(sub_list)

    return date_splits


def split_list(lst: List[T], n: int) -> List[List[T]]:
    """Split list ``lst`` into ``n`` roughly equal parts.

    Args:
        lst: The list to split.
        n: Number of parts.

    Returns:
        A list of ``n`` sub-lists (some may be shorter by at most one element).

    Example:
        >>> split_list([1, 2, 3, 4, 5, 6, 7], 3)
        [[1, 2, 3], [4, 5, 6], [7]]
    """
    avg, extra = divmod(len(lst), n)
    iter_lst = iter(lst)
    return [list(islice(iter_lst, avg + (i < extra))) for i in range(n)]
