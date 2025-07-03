import requests
from bs4 import BeautifulSoup
import csv
URL = "https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

all_movies = soup.select("h2 strong")

movie_titles = [movie.getText() for movie in all_movies]
movie_titles.reverse()

with open("movies.csv", mode="w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["index", "title", "year"])
    for index, movie in enumerate(movie_titles):
        split_index = movie.split(") ")
        movie_index = split_index[0]
        split_year = split_index[1].split(" (")
        movie_title = split_year[0]
        movie_year = split_year[1].replace(")", "")
        writer.writerow([movie_index, movie_title, movie_year])