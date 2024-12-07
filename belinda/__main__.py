"""Main"""

from .shell import ask_for_zpl_path, welcome, console
from .local_playlist import LocalPlaylist
from .playlist_reader import read_zpl_playlist, PlaylistReaderError
from .env_reader import read_credentials, EnvReaderError
from .spotify_credentials import SpotifyCredentials
from .spotify_api import login, logout, search_for_track, SpotifyAPIError


def main() -> None:
    """Main"""
    try:
        welcome()

        credentials: SpotifyCredentials = read_credentials()
        zpl_path: str = ask_for_zpl_path("Enter the path to the .zpl file: ")
        playlist: LocalPlaylist = read_zpl_playlist(zpl_path)

        login(credentials)

        for track in playlist.tracks:
            uri: str = search_for_track(track)
            if uri is not None:
                console.print(f"Found: {track.title or track.pathname} -> {uri}")
            else:
                console.print(
                    f"Not Found: {track.title or track.pathname}", style="yellow"
                )

        logout()

    except KeyboardInterrupt:
        console.print("\n\nInterrupted by user.", style="red")

    except PlaylistReaderError as error:
        console.print(f"\n\n{error}", style="red")

    except EnvReaderError as error:
        console.print(f"\n\n{error}", style="red")

    except SpotifyAPIError as error:
        console.print(f"\n\n{error}", style="red")


if __name__ == "__main__":
    main()
