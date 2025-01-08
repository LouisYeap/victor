import traceback
import tqdm
from typing import Callable, Dict, List, Union, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed, Future


from multiprocessing import Manager, Pool


def thread_pool_executor(
    func: Callable[..., Any],
    tasks: List[Union[Any, Tuple[Any, ...], List[Any]]],
    pool_size: int = 10,
    desc: str = "线程池处理中...",
) -> List[Any]:
    """
    通用多线程任务处理方法

    :param func: 执行任务的函数，接受一个或多个参数
    :param tasks: 任务列表，每个任务可以是单参数，也可以是一个元组或列表（表示多参数）
    :param pool_size: 线程池的大小，默认为 10
    :param desc: 进度条的描述信息，用于显示任务处理进度
    :return: 错误信息列表（如果任务执行无错误，返回空列表）

    使用场景:
    - 对多个任务并行执行时，例如批量下载文件、批量处理数据等。
    - 需要捕获任务中的异常并继续处理后续任务。
    """
    error_msgs = []  # 记录错误信息
    with (
        tqdm.tqdm(total=len(tasks), desc=desc) as pbar,
        ThreadPoolExecutor(max_workers=pool_size) as executor,
    ):
        future_tasks: List[Future[Any]] = [
            (
                executor.submit(func, *task)
                if isinstance(task, (tuple, list))
                else executor.submit(func, task)
            )
            for task in tasks
        ]
        for future in as_completed(future_tasks):
            try:
                if result := future.result():
                    error_msgs.append(result)
            except Exception as e:
                tb = traceback.format_exc()
                error_msg = f"任务出错: {e}\n追溯信息:\n{tb}"
                error_msgs.append(error_msg)
            pbar.update(1)
    return error_msgs


def process_pool_executor(
    func: Callable[..., Any],
    tasks: List[Union[Any, Tuple[Any, ...], List[Any]]],
    pool_size: int = 4,
    shared_variable: Any = None,
    lock=None,
    desc: str = "进程池处理中...",
) -> Dict[str, List[Any]]:
    """
    通用多进程任务处理方法，支持不同类型的共享变量和可选的锁

    :param func: 执行任务的函数，接受一个或多个参数
    :param tasks: 任务列表，每个任务可以是单参数，也可以是一个元组或列表（表示多参数）
    :param pool_size: 进程池的大小，默认为 4
    :param shared_variable: 可选的共享变量（可以是字典、列表或单一值），任务中可以使用
    :param lock: 可选的锁对象，如果传递了锁，任务将对共享变量的访问加锁
    :param desc: 进度条的描述信息，用于显示任务处理进度
    :return: 包含结果列表和错误信息列表的字典 {'results': [], 'errors': []}

    使用场景:
    - 对多个任务并行执行时，某些任务可能需要共享不同类型的变量，并且这些变量需要加锁保护。
    - 需要捕获任务中的异常并记录详细的错误信息。
    """
    with Manager() as manager:
        # 根据共享变量的类型创建合适的共享对象
        if isinstance(shared_variable, dict):
            shared_variable = manager.dict(shared_variable)
        elif isinstance(shared_variable, list):
            shared_variable = manager.list(shared_variable)
        elif isinstance(shared_variable, (int, float, bool)):
            shared_variable = manager.Value(
                type(shared_variable), shared_variable
            )  # 支持共享的原始类型
        elif shared_variable is not None:
            raise TypeError(
                "共享变量类型不支持，只支持字典、列表或基本类型（int、float、bool）。"
            )

        results = manager.list()  # 存储成功结果

        error_msgs = manager.list()  # 存储错误信息

        def worker(task: Union[Any, Tuple[Any, ...], List[Any]]):
            """工作函数，执行任务并根据是否有共享变量来修改它"""
            try:
                # 动态判断是否需要共享变量
                if shared_variable is not None:
                    if lock:
                        with lock:  # 获取锁
                            result = (
                                func(*task, lock, shared_variable=shared_variable)
                                if isinstance(task, (tuple, list))
                                else func(task, lock, shared_variable=shared_variable)
                            )
                    else:
                        result = (
                            func(*task, shared_variable=shared_variable)
                            if isinstance(task, (tuple, list))
                            else func(task, shared_variable=shared_variable)
                        )
                else:
                    result = (
                        func(*task) if isinstance(task, (tuple, list)) else func(task)
                    )

                results.append(result)  # 记录成功结果
            except Exception as e:
                # 捕获异常并记录详细错误信息
                tb = traceback.format_exc()
                error_msg = f"任务出错: {e}\n追溯信息:\n{tb}"
                error_msgs.append(error_msg)

        # 使用进程池处理任务
        with Pool(processes=pool_size) as pool:
            for task in tasks:
                pool.apply_async(worker, args=(task,))  # 异步提交任务

            pool.close()  # 停止接收新任务
            pool.join()  # 等待所有任务完成

        # 返回结果和错误信息
        return {
            "results": list(results),
            "errors": list(error_msgs),
            "shared_variable": shared_variable,
        }
