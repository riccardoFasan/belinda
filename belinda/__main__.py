"""Main"""

from .shell import ask_for_zpl_path, welcome, console, print_comparison_table
from .local_playlist import LocalPlaylist
from .playlist_reader import read_zpl_playlist, PlaylistReaderError
from .env_reader import read_credentials, EnvReaderError
from .spotify_credentials import SpotifyCredentials
from .spotify_api import login, logout, search_for_track, SpotifyAPIError
from .track_results_diffs import TrackResultDiff


def main() -> None:
    """Main"""
    try:
        welcome()

        credentials: SpotifyCredentials = read_credentials()
        zpl_path: str = ask_for_zpl_path("Enter the path to the .zpl file: ")
        playlist: LocalPlaylist = read_zpl_playlist(zpl_path)

        login(credentials)

        diffs = [
            TrackResultDiff(track=track, result=search_for_track(track))
            for track in playlist.tracks
            if track.title
        ]

        print_comparison_table(diffs)

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
