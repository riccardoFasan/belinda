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

PLAYLIST_UPDATE_TRACKS_LIMIT: int = 100


def login(credentials: SpotifyCredentials) -> None:
    """Authenticate on Spotify."""
    global _spotify
    with console.status("[bold green]Authenticating on Spotify..."):
        _spotify = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=credentials.client_id,
                client_secret=credentials.client_secret,
                redirect_uri=REDIRECT_URI,
                scope="playlist-read-private,playlist-modify-private",
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


def create_or_update_playlist(name: str, tracks: list[SpotifyResult]) -> Optional[str]:
    """Create or update a playlist on Spotify."""
    if _spotify is None:
        raise SpotifyAPIError("Spotify not authenticated.")

    with console.status(f"[bold green]Creating or updating playlist {name}..."):
        user_id = _spotify.me()["id"]
        playlists = _spotify.user_playlists(user_id)["items"]

        existing_playlist = None

        for playlist in playlists:
            if playlist["name"] == name:
                existing_playlist = playlist
                break


        selected_playlist = existing_playlist or _spotify.user_playlist_create(
            user_id, name, public=False
        )

        _spotify.playlist_replace_items(selected_playlist["id"], [])

        filtered_uris = []
        for track in tracks:
            if track.uri not in filtered_uris:
                filtered_uris.append(track.uri)

        for i in range(0, len(filtered_uris), PLAYLIST_UPDATE_TRACKS_LIMIT):
            uris = [uri for uri in filtered_uris[i : i + PLAYLIST_UPDATE_TRACKS_LIMIT]]
            _spotify.playlist_add_items(selected_playlist["id"], uris)

        return selected_playlist["uri"]


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
