import os
from typing import TypeVar, Union

T = TypeVar("T")

R = TypeVar("R")

IMAGE_FILE_EXTENSIONS = [
    "apng",
    "png",
    "avif",
    "gif",
    "jpg",
    "jpeg",
    "jfif",
    "jp2",
    "j2k",
    "jpf",
    "jpx",
    "jpm",
    "mj2",
    "pjpeg",
    "pjp",
    "png",
    "svg",
    "webp",
    "bmp",
    "ico",
    "cur",
    "tif",
    "tiff",
    "heif",
    "heic",
    "eps",
]

PathLike = Union[str, os.PathLike]
