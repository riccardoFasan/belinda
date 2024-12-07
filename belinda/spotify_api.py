"""Spofify API module."""

from typing import Optional
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from .shell import console
from .spotify_credentials import SpotifyCredentials
from .local_playlist import LocalTrack

_spotify: Optional[Spotify] = None
REDIRECT_URI: str = "http://localhost:8888/callback"


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


def search_for_track(track: LocalTrack) -> Optional[str]:
    """Search for a track and return its URI."""
    if _spotify is None:
        raise SpotifyAPIError("Spotify not authenticated.")

    with console.status(
        f"[bold green]Searching for {track.title or track.pathname}..."
    ):

        query = _build_track_query(track)

        results = _spotify.search(q=query, limit=1)
        if results["tracks"]["items"]:
            return results["tracks"]["items"][0]["uri"]

    return None


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
