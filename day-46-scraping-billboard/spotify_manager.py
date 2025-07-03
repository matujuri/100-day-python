import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import requests
import webbrowser

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
TOKEN = os.getenv("SPOTIFY_TOKEN")
USER_ID = os.getenv("SPOTIFY_USER_ID")

def get_track_uri(track_name) -> str | None:
    response = requests.get(
        url=f'https://api.spotify.com/v1/search?q={track_name}&type=track&limit=1',
        headers={
            'Authorization': f'Bearer {TOKEN}'
        }
    )
    if response.status_code == 200 and response.json()['tracks']['items']:
        return response.json()['tracks']['items'][0]['uri']
    else:
        return None
    
def add_track_to_playlist(track_uri: str, playlist_id: str):
    response = requests.post(
        url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks',
        headers={
            'Authorization': f'Bearer {TOKEN}'
        },
        json={
            'uris': [track_uri]
        }
    )
    print(response.json())
    
def create_playlist(memory_day: str) -> str:
    response = requests.post(
        url=f'https://api.spotify.com/v1/users/{USER_ID}/playlists',
        headers={
            'Authorization': f'Bearer {TOKEN}'
        },
        json={
            'name': f'{memory_day} Billboard 100',
            'description': f'100 music from {memory_day}',
            'public': False
        }
    )
    return response.json()["id"]

def open_playlist_in_browser(playlist_id: str):
    webbrowser.open(f"https://open.spotify.com/playlist/{playlist_id}")
    

# First, authenticate in spotify_manager.py, then save token to .env file
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
        
# authenticate()