"""Shell utilities."""

from art import tprint
from rich.console import Console
from rich.table import Table
from .filesystem import is_zpl_file
from .track_results_diffs import TrackResultDiff
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


def print_comparison_table(diffs: list[TrackResultDiff]) -> None:
    """
    Print results and playlist table.
    """
    table = Table(title="Results and Playlist")
    table.add_column("Playlist Track", header_style="cyan")
    table.add_column("Spotify Track", header_style="green")

    for diff in diffs:
        table.add_row(
            diff.track.pathname,
            diff.result.title if diff.result else "Not found",
            style="red" if diff.result is None else None,
        )

    console.print(table)
