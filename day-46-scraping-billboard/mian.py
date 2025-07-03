import requests
from bs4 import BeautifulSoup
from spotify_manager import get_track_uri, add_track_to_playlist, open_playlist_in_browser, create_playlist

# Firstly, authenticate in spotify_manager.py, then save token to .env file

memory_day = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD: ")

PLAYLIST_ID = create_playlist(memory_day)

def get_track_names_from_billboard(memory_day) -> list[str]:
    URL = f"https://www.billboard.com/charts/hot-100/{memory_day}"

    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"})
    website_html = response.text

    soup = BeautifulSoup(website_html, "html.parser")
    song_name_h3 = soup.select(selector="li h3#title-of-a-story")

    return [song.getText().strip() for song in song_name_h3]

# get song names from billboard
track_names = get_track_names_from_billboard(memory_day)

# get track uris from spotify
track_uris = [get_track_uri(track) for track in track_names if get_track_uri(track)]

# add track uris to playlist
for track_uri in track_uris:
    add_track_to_playlist(track_uri, PLAYLIST_ID)

# open playlist in browser after adding tracks
open_playlist_in_browser(PLAYLIST_ID)