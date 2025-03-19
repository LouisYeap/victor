import subprocess
from typing import Optional


def execute_command(
    cmd: str, max_retries: int = 1, switch: bool = False
) -> Optional[str]:
    """
    执行命令行函数

    参数:
        cmd (str): 要执行的 shell 命令。
        max_retries (int): 如果命令失败，最大重试次数（默认值: 1)。

    返回:
        Optional[str]: 如果命令成功返回 None;如果重试次数耗尽仍失败,返回失败的命令字符串。
    """
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                check=True,  # 让 `subprocess.run()` 自动抛出异常
            )

            # if result.returncode == 0:
            #     if switch:
            #         print(result.stdout.strip()) if result.stdout else None
            #     return None
            # print(f"Attempt {attempt + 1} failed for command: {cmd}")
            # print(f"Error: {result.stderr.strip()}")
            # if attempt < max_retries - 1:
            #     print("Retrying...")

            # 如果 switch=True，返回 stdout，否则返回 None（表示成功）
            return result.stdout.strip() if switch else None

        except subprocess.CalledProcessError as e:
            print(f"❌命令执行失败 (尝试 {attempt + 1}/{max_retries}):{cmd}")
            print(f"❌ 错误信息: {e.stderr.strip()}")
            if attempt < max_retries - 1:
                print("🔄 重试中...")
    return cmd
