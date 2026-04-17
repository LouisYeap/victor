"""Public type aliases for Victor."""

from __future__ import annotations

from os import PathLike
from typing import Union

__all__ = ("PathLike",)


PathLike = Union[str, PathLike]
"""Type alias for path-like arguments — accepts ``str`` or ``os.PathLike``."""
