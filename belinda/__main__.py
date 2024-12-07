"""Main"""

from asyncio import run
from .shell import (
    ask_for_zpl_or_m3u8_path,
    welcome,
    console,
    print_comparison_table,
    ask_for_confirmation,
)
from .filesystem import is_zpl_file
from .local_playlist import LocalPlaylist
from .playlist_reader import read_zpl_playlist, read_m3u_playlist, PlaylistReaderError
from .env_reader import read_credentials, EnvReaderError
from .spotify_credentials import SpotifyCredentials
from .spotify_api import (
    login,
    logout,
    search_for_tracks,
    create_or_update_playlist,
    SpotifyAPIError,
)
from .track_results_diffs import TrackResultDiff


async def main() -> None:
    """Main"""
    try:
        welcome()

        credentials: SpotifyCredentials = read_credentials()
        zpl_path: str = ask_for_zpl_or_m3u8_path(
            "Enter the path to the .zpl or .m3u8 file: "
        )
        playlist: LocalPlaylist = (
            read_zpl_playlist(zpl_path)
            if is_zpl_file(zpl_path)
            else read_m3u_playlist(zpl_path)
        )

        login(credentials)

        diffs: list[TrackResultDiff] = await search_for_tracks(playlist.tracks)

        print_comparison_table(diffs)

        should_create_playlist: bool = ask_for_confirmation(
            "Do you want to create a playlist with the found tracks?"
        )

        if should_create_playlist:
            results: list[str] = [diff.result for diff in diffs if diff.result]
            uri = create_or_update_playlist(playlist.name, results)
            if uri:
                console.print(f"\n\nPlaylist created: {uri}")
            else:
                console.print("\n\nPlaylist not created.", style="red")

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
    run(main())
