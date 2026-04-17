"""Exports package version."""

from importlib import metadata

__all__ = ("__version__",)

try:
    __version__ = metadata.version("victor-utils")
except metadata.PackageNotFoundError:
    __version__ = "1.0.0"
