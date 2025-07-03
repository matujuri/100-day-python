import requests
from bs4 import BeautifulSoup
import csv
import time

INPUT_CSV = 'movies.csv'
OUTPUT_CSV = 'movies_with_vod.csv'
BASE_SEARCH_URL = 'https://filmarks.com/search/movies/?q='

def fetch_vod_services(title):
    url = BASE_SEARCH_URL + requests.utils.quote(title)
    resp = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    first_movie = soup.select_one('.p-content-cassette')
    vods = first_movie.select('.p-content-cassette-vod__title')
    services = [vod.get_text(strip=True) for vod in vods]
    return ', '.join(services)

def main():
    with open(INPUT_CSV, newline='', encoding='utf-8') as fr, \
         open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as fw:
        reader = csv.DictReader(fr)
        fieldnames = reader.fieldnames + ['VOD']
        writer = csv.DictWriter(fw, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            title = row['title']
            try:
                vod = fetch_vod_services(title)
                print(f"{title}: {vod}")
            except Exception as e:
                vod = ''
                print(f"Error fetching {title}: {e}")
            row['VOD'] = vod
            writer.writerow(row)
            time.sleep(1)

if __name__ == '__main__':
    main()