"""Main"""

from .shell import ask_for_zpl_path, welcome, console
from .local_playlist import LocalPlaylist
from .playlist_reader import read_zpl_playlist, PlaylistReaderError
from .env_reader import read_credentials, EnvReaderError
from .spotify_credentials import SpotifyCredentials


def main() -> None:
    """Main"""
    try:
        welcome()

        credentials: SpotifyCredentials = read_credentials()
        zpl_path: str = ask_for_zpl_path("Enter the path to the .zpl file: ")
        playlist: LocalPlaylist = read_zpl_playlist(zpl_path)

    except KeyboardInterrupt:
        console.print("\n\nInterrupted by user.", style="red")

    except PlaylistReaderError as error:
        console.print(f"\n\n{error}", style="red")

    except EnvReaderError as error:
        console.print(f"\n\n{error}", style="red")


if __name__ == "__main__":
    main()
