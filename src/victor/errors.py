"""Custom exceptions for Victor."""

from __future__ import annotations

from enum import Enum
from typing import List, Optional


class ErrorCode(Enum):
    """Victor error codes for programmatic error handling."""

    FILE_NOT_FOUND = "VICTOR_FILE_NOT_FOUND"
    INVALID_JSON = "VICTOR_INVALID_JSON"
    INVALID_YAML = "VICTOR_INVALID_YAML"
    INVALID_TYPE = "VICTOR_INVALID_TYPE"
    COMMAND_FAILED = "VICTOR_COMMAND_FAILED"
    PARALLEL_EXECUTION_ERROR = "VICTOR_PARALLEL_EXECUTION_ERROR"


class VictorError(Exception):
    """Base exception for all Victor errors."""

    pass


class FileNotFoundError(VictorError):
    """Raised when a required file does not exist."""

    pass


class InvalidJSONError(VictorError):
    """Raised when JSON decoding fails."""

    pass


class InvalidYAMLError(VictorError):
    """Raised when YAML parsing fails."""

    pass


class InvalidTypeError(VictorError):
    """Raised when a value has an unexpected type."""

    def __init__(
        self,
        message: str,
        *,
        expected_type: Optional[str] = None,
        received_type: Optional[str] = None,
    ) -> None:
        self.expected_type = expected_type
        self.received_type = received_type
        detail = f" (expected {expected_type}, got {received_type})" if (expected_type and received_type) else ""
        super().__init__(message + detail)


class CommandFailedError(VictorError):
    """Raised when a shell command returns a non-zero exit code."""

    def __init__(self, message: str, cmd: str = "") -> None:
        self.message = message
        self.cmd = cmd
        super().__init__(message + (f" (cmd: {cmd})" if cmd else ""))


class ParallelExecutionError(VictorError):
    """Raised when parallel task execution encounters failures."""

    def __init__(self, errors: List[str]) -> None:
        self.errors = errors
        super().__init__(f"{len(errors)} task(s) failed during parallel execution")