import requests
from bs4 import BeautifulSoup

input_year = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{input_year}"

response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"})
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")
song_name_h3 = soup.select(selector="li h3#title-of-a-story")

song_names = [song.getText().strip() for song in song_name_h3]

print(song_names)