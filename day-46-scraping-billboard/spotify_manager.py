import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import requests
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
TOKEN = os.getenv("SPOTIFY_TOKEN")
USER_ID = os.getenv("SPOTIFY_USER_ID")
PLAYLIST_NAME = "2011-01-01 Billboard 100"
PLAYLIST_ID = os.getenv("SPOTIFY_PLAYLIST_ID")

def get_song_link(song_name) -> str | None:
    response = requests.get(
        url=f'https://api.spotify.com/v1/search?q={song_name}&type=track&limit=1',
        headers={
            'Authorization': f'Bearer {TOKEN}'
        }
    )
    if response.status_code == 200 and response.json()['tracks']['items']:
        return response.json()['tracks']['items'][0]['uri']
    else:
        return None
    
def add_song_to_playlist(song_link: str):
    response = requests.post(
        url=f'https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks',
        headers={
            'Authorization': f'Bearer {TOKEN}'
        },
        json={
            'uris': [song_link]
        }
    )
    print(response.json())

def authenticate():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='https://example.com',
        scope='user-library-read playlist-modify-private playlist-modify-public',
        show_dialog=True,
        cache_path='day-46-scraping-billboard/token.txt'
    ))

    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'], '-', track['artists'][0]['name'])
    
def create_playlist():
    response = requests.post(
        url=f'https://api.spotify.com/v1/users/{USER_ID}/playlists',
        headers={
            'Authorization': f'Bearer {TOKEN}'
        },
        json={
            'name': PLAYLIST_NAME,
            'description': '100 music from date in past',
            'public': False
        }
    )
    print(response.json()["id"])
