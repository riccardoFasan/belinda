"""Main"""

from .shell import ask_for_zpl_path, welcome, console
from .local_playlist import LocalPlaylist
from .playlist_reader import read_zpl_playlist, PlaylistReaderError


def main() -> None:
    """Main"""
    try:
        welcome()

        zpl_path: str = ask_for_zpl_path("Enter the path to the .zpl file: ")
        playlist: LocalPlaylist = read_zpl_playlist(zpl_path)
        print(playlist)

    except KeyboardInterrupt:
        console.print("\n\nInterrupted by user.", style="red")

    except PlaylistReaderError:
        console.print("\n\nInvalid .zpl file.", style="red")


if __name__ == "__main__":
    main()
