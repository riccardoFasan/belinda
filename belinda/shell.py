"""Shell utilities."""

from art import tprint
from rich.console import Console
from .filesystem import is_zpl_file
from . import __version__

console = Console()


def welcome() -> None:
    """
    Print welcome message
    """
    print("\n\n")
    tprint("belinda")
    print(f"version {__version__}\n\n")


def ask_for_zpl_path(text: str) -> str:
    """
    Ask user for a path, check if is a zpl and return it trailed.
    """
    while True:
        file_path = input(text)
        if is_zpl_file(file_path):
            return file_path
        console.print(f"{file_path} is not a valid .zpl file.", style="red")


def ask_for_confirmation(text: str, default=True) -> bool:
    """
    Ask user for a confirmation with y/n style and return it.
    (default is prompt with uppercase)
    """
    sample: str = "Y/n" if default else "N/y"
    while True:
        answer = input(f"{text} [{sample}]: ")
        if not answer:
            return default
        if answer.lower() == "y":
            return True
        if answer.lower() == "n":
            return False
        console.print("Invalid answer, please type 'y' or 'n'.", style="red")
