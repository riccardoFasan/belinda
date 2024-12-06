"""Module for reading zpl playlists"""

import xml.etree.ElementTree as xml
from typing import Optional
from .local_playlist import LocalPlaylist, LocalTrack
from .shell import console


def read_zpl_playlist(local_path: str) -> LocalPlaylist:
    """Reads a .zpl file and returns a LocalPlaylist object."""

    with console.status(f"[bold green]Scanning {local_path}..."):

        root: Optional[xml.Element] = xml.parse(local_path).getroot()

        if root is None:
            raise ValueError("Invalid .zpl file.")

        head: Optional[xml.Element] = root.find("head")
        if head is None:
            raise ValueError("Invalid .zpl file.")

        title: Optional[xml.Element] = head.find("title")
        if title is None:
            raise ValueError("Invalid .zpl file.")

        name: Optional[str] = title.text or 'Untitled Playlist'

        body: Optional[xml.Element] = root.find("body")

        if body is None:
            raise ValueError("Invalid .zpl file.")

        seq: Optional[xml.Element] = body.find("seq")
        if seq is None:
            raise ValueError("Invalid .zpl file.")

        tracks: list[LocalTrack] = []

        for src in seq.findall("media"):
            track_path: Optional[str] = src.get("src")
            if track_path is not None:
                tracks.append(LocalTrack(track_path))

        return LocalPlaylist(name=name, tracks=tracks)
