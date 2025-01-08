import traceback
import tqdm
from typing import Callable, List, Union, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed, Future


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
