"""Module for reading Spotify credentials from .env file"""

from dotenv import dotenv_values
from .spotify_credentials import SpotifyCredentials


def read_credentials() -> SpotifyCredentials:
    """Reads Spotify credentials from .env file"""
    # load_dotenv(override=False)
    values = dotenv_values(".env")

    client_id = values["SPOTIFY_CLIENT_ID"]
    client_secret = values["SPOTIFY_CLIENT_SECRET"]
    if client_id is None or client_secret is None:
        raise EnvReaderError(
            "SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET not found in .env file"
        )

    return SpotifyCredentials(client_id, client_secret)


class EnvReaderError(ValueError):
    """Custom error for EnvReader"""
