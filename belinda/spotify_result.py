"""Spotify search results models"""

from dataclasses import dataclass


@dataclass
class SpotifyResult:
    """SpotifyResult model"""

    title: str
    artist: str
    album: str
    uri: str
    href: bool
