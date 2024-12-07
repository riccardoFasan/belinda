"""SpotifyCredentials models"""

from dataclasses import dataclass


@dataclass
class SpotifyCredentials:
    """SpotifyCredentials model"""

    client_id: str
    client_secret: str
