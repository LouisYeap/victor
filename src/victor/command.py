"""Shell command execution utilities.

Example:
    >>> from victor.command import execute_command
    >>> execute_command("echo hello", switch=True)
    'hello'
"""

from __future__ import annotations

import subprocess
import traceback
from typing import Optional

__all__ = ("execute_command",)


def execute_command(
    cmd: str,
    *,
    max_retries: int = 1,
    switch: bool = False,
    timeout: float | None = None,
) -> Optional[str]:
    """Execute a shell command with optional retry and timeout.

    Args:
        cmd: The shell command to execute.
        max_retries: Maximum retry attempts on failure (default 1).
        switch: If ``True``, return stdout as string on success;
                if ``False``, return ``None`` on success.
                On final failure, always returns the command string.
        timeout: Maximum time in seconds before killing the process (default None = no limit).

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
                timeout=timeout,
            )
            return result.stdout.strip() if switch else None

        except subprocess.TimeoutExpired as e:
            print(f"[!] Command timed out after {timeout}s: {cmd}")
            raise
        except subprocess.CalledProcessError as e:
            print(f"[!] Command failed (attempt {attempt + 1}/{max_retries}): {cmd}")
            print(f"[!] stderr: {e.stderr.strip()}")
            traceback.print_exc()
            if attempt < max_retries - 1:
                print("[*] Retrying...")

    return cmd
