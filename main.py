#import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import billboard

scope = "playlist-modify-public"

client_id = os.environ.get("SPOTIPY_CLIENT_ID")
client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.environ.get("SPOTIPY_REDIRECT_URI")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
    )
)


def add_billboard_songs_to_new_playlist():
    playlist_date = input("Enter the date[YYYY-MM-DD] you want to make playlist of: ")
    chart = billboard.ChartData(name='hot-100', date=playlist_date)
    tracks = [track for track in chart]

    # Create new playlist
    playlist_name = "Billboard Top 100 : " + playlist_date
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name)

    # Add tracks to playlist
    track_uris = []
    for track in tracks:
        result = sp.search(q=track, type='track,artist')
        if result['tracks']['items']:
            track_uri = result['tracks']['items'][0]['uri']
            track_uris.append(track_uri)

    sp.playlist_add_items(playlist['id'], track_uris)


def add_song_to_new_playlist(song):
    playlist_name = input("Name of your Playlist: ")
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name)
    result = sp.search(q=song, type='track,artist')
    if result['tracks']['items']:
        url = result['tracks']['items'][0]['uri']
        sp.playlist_add_items(playlist['id'], [url])


# add_billboard_songs_to_new_playlist()
track = "'Fastlove' by George Michael"
add_song_to_new_playlist(track)
