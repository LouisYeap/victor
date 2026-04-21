"""Shell command execution utilities.

Example:
    >>> from victor.command import execute_command
    >>> execute_command("echo hello", switch=True)
    'hello'
"""

from __future__ import annotations

import subprocess
import traceback
from typing import Union

__all__ = ("execute_command",)


def execute_command(
    cmd: str,
    max_retries: int = 1,
    switch: bool = False,
) -> Union[str, None]:
    """Execute a shell command with optional retry.

    Args:
        cmd: The shell command to execute.
        max_retries: Maximum retry attempts on failure (default 1).
        switch: If ``True``, return stdout as string on success;
                if ``False``, return ``None`` on success.
                On final failure, always returns the command string.

    Returns:
        - ``None`` on success (when ``switch=False``).
        - stdout string on success (when ``switch=True``).
        - The command string itself on final failure.
    """
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                check=True,
            )
            return result.stdout.strip() if switch else None

        except subprocess.CalledProcessError as e:
            print(f"[!] Command failed (attempt {attempt + 1}/{max_retries}): {cmd}")
            print(f"[!] stderr: {e.stderr.strip()}")
            traceback.print_exc()
            if attempt < max_retries - 1:
                print("[*] Retrying...")

    return cmd