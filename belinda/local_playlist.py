"""Local playlist dataclasses."""

from dataclasses import dataclass


@dataclass
class LocalTrack:
    """
    Local track dataclass.
    """

    path: str


@dataclass
class LocalPlaylist:
    """
    Local playlist dataclass.
    """

    name: str
    tracks: list[LocalTrack]
