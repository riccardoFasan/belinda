"""Local playlist and Spotify results comparison models"""

from typing import Optional
from dataclasses import dataclass
from .local_playlist import LocalTrack
from .spotify_result import SpotifyResult


@dataclass
class TrackResultDiff:
    """
    TrackResultDiff dataclass.
    """

    track: LocalTrack
    result: Optional[SpotifyResult]
