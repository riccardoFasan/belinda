"""Local playlist models"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class LocalTrack:
    """
    Local track dataclass.
    """

    path: str
    pathname: str
    artist: Optional[str]
    album: Optional[str]
    title: Optional[str]


@dataclass
class LocalPlaylist:
    """
    Local playlist dataclass.
    """

    name: str
    tracks: list[LocalTrack]
