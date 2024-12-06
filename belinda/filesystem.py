"""Filesystem utilities."""

from os import path


def is_zpl_file(file_path: str) -> bool:
    """
    Check if a file is a ZPL file.
    """
    return path.isfile(file_path) and path.splitext(file_path)[1].lower() == ".zpl"
