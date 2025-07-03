import requests
from bs4 import BeautifulSoup
from spotify_manager import get_song_link, add_song_to_playlist

input_year = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD: ")

def get_song_names_from_billboard(input_year) -> list[str]:
    URL = f"https://www.billboard.com/charts/hot-100/{input_year}"

    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"})
    website_html = response.text

    soup = BeautifulSoup(website_html, "html.parser")
    song_name_h3 = soup.select(selector="li h3#title-of-a-story")

    return [song.getText().strip() for song in song_name_h3]

song_names = get_song_names_from_billboard(input_year)
song_links = [get_song_link(song) for song in song_names if get_song_link(song)]
for song_link in song_links:
    add_song_to_playlist(song_link)
