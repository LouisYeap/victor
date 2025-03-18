import traceback
import tqdm
from typing import Callable, Dict, List, Union, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
import os

from multiprocessing import Pool


# def thread_pool_executor(
#     func: Callable[..., Any],
#     tasks: List[Union[Any, Tuple[Any, ...], List[Any]]],
#     pool_size: int = 60,
#     desc: str = "线程池处理中...",
# ) -> Dict[str, List[Any]]:
#     """
#     通用多线程任务处理方法

#     :param func: 执行任务的函数，接受一个或多个参数
#     :param tasks: 任务列表，每个任务可以是单参数，也可以是一个元组或列表（表示多参数）
#     :param pool_size: 线程池的大小，默认为 10
#     :param desc: 进度条的描述信息，用于显示任务处理进度
#     :return: 错误信息列表（如果任务执行无错误，返回空列表）


#     使用场景:
#     - 对多个任务并行执行时，例如批量下载文件、批量处理数据等。
#     - 需要捕获任务中的异常并继续处理后续任务。
#     """
#     results = []  # 记录成功结果
#     error_msgs = []  # 记录错误信息
#     # with (
#     #     tqdm.tqdm(total=len(tasks), desc=desc) as pbar,
#     #     ThreadPoolExecutor(max_workers=pool_size) as executor,
#     # ):
#     with tqdm.tqdm(total=len(tasks), desc=desc) as pbar:
#         with ThreadPoolExecutor(max_workers=pool_size) as executor:
#             future_tasks: List[Future[Any]] = [
#                 (
#                     executor.submit(func, *task)
#                     if isinstance(task, (tuple, list))
#                     else executor.submit(func, task)
#                 )
#                 for task in tasks
#             ]
#             for future in as_completed(future_tasks):
#                 try:
#                     result = future.result()
#                     # if result := future.result():
#                     if result:
#                         results.append(result)
#                         # results.append(result)
#                 except Exception as e:
#                     tb = traceback.format_exc()
#                     error_msg = f"任务出错: {e}\n追溯信息:\n{tb}"
#                     error_msgs.append(error_msg)
#                 pbar.update(1)
#         return {"results": results, "errors": error_msgs}


def thread_pool_executor(
    func: Callable[..., Any],
    tasks: List[Union[Any, Tuple[Any, ...], List[Any]]],
    pool_size: int = 60,
    desc: str = "线程池处理中...",
) -> Dict[str, List[Any]]:
    """
    通用多线程任务处理方法

    :param func: 执行任务的函数，接受一个或多个参数
    :param tasks: 任务列表，每个任务可以是单参数，也可以是一个元组或列表（表示多参数）
    :param pool_size: 线程池的大小，默认为 60
    :param desc: 进度条的描述信息，用于显示任务处理进度
    :return: 包含结果和错误信息的字典 {'results': [], 'errors': []}

    适用场景：
    - 适用于 I/O 密集型任务（如批量下载、爬虫、数据处理）。
    - 需要捕获任务中的异常，并继续执行后续任务。

    使用示例：
    >>> def square(x):
    >>>     return x * x
    >>> tasks = [1, 2, 3, 4, 5]
    >>> result = thread_pool_executor(square, tasks)
    >>> print(result["results"])  # [1, 4, 9, 16, 25]
    """

    results = []  # 存储成功结果
    error_msgs = []  # 存储错误信息

    with tqdm.tqdm(total=len(tasks), desc=desc, leave=True) as pbar:
        with ThreadPoolExecutor(max_workers=pool_size) as executor:
            # 提交任务
            future_tasks: List[Future[Any]] = [
                executor.submit(
                    func, *task if isinstance(task, (tuple, list)) else (task,)
                )
                for task in tasks
            ]

            for future in as_completed(future_tasks):
                try:
                    result = future.result()
                    if result is not None:  # 确保不会丢失 0、False 等有效返回值
                        results.append(result)
                except Exception as e:
                    error_msgs.append(
                        f"任务出错: {type(e).__name__}: {e}\n{traceback.format_exc()}"
                    )

                pbar.update(1)  # 更新进度条

    return {"results": results, "errors": error_msgs}


def process_pool_executor(
    func: Callable[..., Any],
    tasks: List[Union[Any, Tuple[Any, ...], List[Any]]],
    pool_size: int = 8,  # 让 `pool_size=None` 时自动匹配 CPU 核心数
    desc: str = "进程池处理中...",
) -> Dict[str, List[Any]]:
    """
    使用 `multiprocessing.Pool` 并行执行任务，并获取返回值，带 `tqdm` 进度条。

    :param func: 需要并行执行的函数
    :param tasks: 任务列表，每个任务可以是单参数，也可以是一个元组/列表（多参数）
    :param pool_size: 进程池大小，默认为 `os.cpu_count()`(CPU 核心数）
    :param desc: 进度条描述信息
    :return: 字典 {'results': 任务返回值列表, 'errors': 错误信息列表}

    适用场景：
    - 计算密集型任务（如数据处理、深度学习计算）
    - 大量独立任务的并行执行（如批量图像处理）

    使用示例：
    >>> def square(x):
    >>>     return x * x
    >>> tasks = [1, 2, 3, 4, 5]
    >>> result = process_pool_executor(square, tasks)
    >>> print(result["results"])  # [1, 4, 9, 16, 25]
    """

    if pool_size is None:
        pool_size = os.cpu_count() or 8  # 获取 CPU 核心数，默认 8

    results = []
    error_msgs = []

    with Pool(processes=pool_size) as pool:
        future_results = [
            pool.apply_async(
                func, args=task if isinstance(task, (tuple, list)) else (task,)
            )
            for task in tasks
        ]

        with tqdm.tqdm(
            total=len(future_results), desc=desc, unit="task", leave=True
        ) as pbar:
            for future in future_results:
                try:
                    results.append(future.get())  # 获取任务返回值
                except Exception as e:
                    tb = traceback.format_exc()
                    error_msgs.append(
                        f"任务 {future} 出错: {type(e).__name__}: {e}\n{tb}"
                    )
                pbar.update(1)  # 更新进度条

    return {"results": results, "errors": error_msgs}
