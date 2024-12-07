"""Filesystem utilities."""

from os import path


def is_m3u8_file(file_path: str) -> bool:
    """
    Check if a file is a M3U8 file.
    """
    return path.isfile(file_path) and path.splitext(file_path)[1].lower() == ".m3u8"


def is_zpl_file(file_path: str) -> bool:
    """
    Check if a file is a ZPL file.
    """
    return path.isfile(file_path) and path.splitext(file_path)[1].lower() == ".zpl"


def is_mp3_file(file_path: str) -> bool:
    """
    Check if a file is a MP3 file.
    """
    return path.isfile(file_path) and path.splitext(file_path)[1].lower() == ".mp3"
