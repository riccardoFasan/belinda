# Belinda

Interactive python script created to automate the creation of Spotify private playlists from .zpl or .m3u8 local playlist files (Windows only).

## Install dependencies

```shell
pipenv install
```

or

```shell
pip install -r requirements.txt
```

## Usage

Get a client id and client secret from the [Spotify Developer Dashboard](https://developer.spotify.com/) and add them to a .env file in the root directory of the project.

```shell
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

Then run the script with the following command (pipenv):

```shell
pipenv run python -m belinda
```

## Fun fact

The Belinda comes from Belinda Carlistle, famous for "Heaven is a place on earth".
I was listening a [cover of this song by the First to Eleven](https://www.youtube.com/watch?v=MjFpRvZLHA0&list=RDMjFpRvZLHA0) when I was thinking about this script.
