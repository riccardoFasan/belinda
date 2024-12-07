"""Spofify API module."""

from asyncio import get_event_loop, AbstractEventLoop, gather, create_task
from typing import Optional
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from .shell import console
from .spotify_credentials import SpotifyCredentials
from .spotify_result import SpotifyResult
from .local_playlist import LocalTrack
from .track_results_diffs import TrackResultDiff

_spotify: Optional[Spotify] = None
REDIRECT_URI: str = "http://localhost:8888/callback"

_loop: Optional[AbstractEventLoop] = None



def login(credentials: SpotifyCredentials) -> None:
    """Authenticate on Spotify."""
    global _spotify
    with console.status("[bold green]Authenticating on Spotify..."):
        _spotify = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=credentials.client_id,
                client_secret=credentials.client_secret,
                redirect_uri=REDIRECT_URI,
                scope="playlist-modify-private",
            )
        )


def logout() -> None:
    """Logout from Spotify."""
    global _spotify
    _spotify = None


async def search_for_tracks(tracks: list[LocalTrack]) -> list[TrackResultDiff]:
    """Search for tracks and return a list of TrackResultDiff."""
    if _spotify is None:
        raise SpotifyAPIError("Spotify not authenticated.")

    global _loop
    _loop = get_event_loop()

    with console.status("[bold green]Searching for tracks..."):
        tasks = [create_task(_search_for_track(track)) for track in tracks]
        diffs = await gather(*tasks)
        return diffs


async def _search_for_track(track: LocalTrack) -> TrackResultDiff:
    """Search for a track and return TrackResultDiff."""
    if _spotify is None:
        raise SpotifyAPIError("Spotify not authenticated.")

    query = _build_track_query(track)

    res = await _loop.run_in_executor(None, _spotify.search, query, 1)
    if res["tracks"]["items"]:
        first_res = res["tracks"]["items"][0]
        if first_res:
            result = SpotifyResult(
                title=first_res["name"],
                artist=first_res["artists"][0]["name"],
                album=first_res["album"]["name"],
                uri=first_res["uri"],
                href=first_res["href"],
            )
            return TrackResultDiff(track=track, result=result)

    return TrackResultDiff(track=track, result=None)


def create_playlist(name: str, tracks: list[SpotifyResult]) -> Optional[str]:
    """Create a playlist on Spotify."""
    if _spotify is None:
        raise SpotifyAPIError("Spotify not authenticated.")

    with console.status(f"[bold green]Creating playlist {name}..."):
        user = _spotify.me()["id"]
        playlist = _spotify.user_playlist_create(user, name, public=False)

        uris = [track.uri for track in tracks]
        _spotify.playlist_add_items(playlist["id"], uris)

        return playlist["uri"]


def _build_track_query(track: LocalTrack) -> str:
    """Build a query string for searching a track."""
    query: str = ""
    if track.title:
        query += f"{track.title} "
    if track.artist:
        query += f"{track.artist} "
    if track.album:
        query += f"{track.album} "

    stripped_query = query.strip()
    if stripped_query:
        return stripped_query

    return track.pathname


class SpotifyAPIError(ValueError):
    """Custom error for SpotifyAPI"""
