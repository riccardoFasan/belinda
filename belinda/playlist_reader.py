"""Module for reading zpl playlists"""

import xml.etree.ElementTree as xml
from typing import Optional
from pathlib import Path
import eyed3
from .local_playlist import LocalPlaylist, LocalTrack
from .shell import console
from .filesystem import is_mp3_file


def read_zpl_playlist(playlist_path: str) -> LocalPlaylist:
    """Reads a .zpl file and returns a LocalPlaylist object."""

    with console.status(f"[bold green]Scanning {playlist_path}..."):

        root: Optional[xml.Element] = xml.parse(playlist_path).getroot()
        if root is None:
            raise PlaylistReaderError("Invalid .zpl file.")

        head: Optional[xml.Element] = root.find("head")
        if head is None:
            raise PlaylistReaderError("Invalid .zpl file.")

        title: Optional[xml.Element] = head.find("title")
        if title is None:
            raise PlaylistReaderError("Invalid .zpl file.")

        name: Optional[str] = title.text or "Untitled Playlist"

        body: Optional[xml.Element] = root.find("body")
        if body is None:
            raise PlaylistReaderError("Invalid .zpl file.")

        seq: Optional[xml.Element] = body.find("seq")
        if seq is None:
            raise PlaylistReaderError("Invalid .zpl file.")

        tracks: dict[str, LocalTrack] = {}

        for src in seq.findall("media"):
            track_path: Optional[str] = src.get("src")
            if track_path is not None:
                if track_path not in tracks:
                    local_track = _read_local_track(track_path)
                    tracks[track_path] = local_track

        return LocalPlaylist(name=name, tracks=list(tracks.values()))


def _read_local_track(track_path: str) -> LocalTrack:
    """Reads a local track and returns a LocalTrack object."""

    pathname: str = Path(track_path).name
    is_mp3: bool = is_mp3_file(track_path)
    if not is_mp3:
        return LocalTrack(
            path=track_path,
            pathname=pathname,
            title=None,
            album=None,
            artist=None,
        )

    audiofile = eyed3.load(track_path)

    if not audiofile:
        return LocalTrack(
            path=track_path,
            pathname=pathname,
            title=None,
            album=None,
            artist=None,
        )

    return LocalTrack(
        path=track_path,
        pathname=pathname,
        title=audiofile.tag.title,
        album=audiofile.tag.album,
        artist=audiofile.tag.artist,
    )


class PlaylistReaderError(ValueError):
    """Custom error for PlaylistReader"""
