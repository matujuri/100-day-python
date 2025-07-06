from bs4 import BeautifulSoup
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_rental_data() -> list[dict]:
    url = "https://appbrewery.github.io/Zillow-Clone/"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    all_cards = soup.find_all(name="div", class_="StyledCard-c11n-8-84")

    rental_data = []

    for card in all_cards:
        address = card.find("address").getText().strip()
        link = card.find(name="a").get("href").strip()
        price = card.find(name="span", class_="PropertyCardWrapper__StyledPriceLine").getText().strip()
        price = price.split("+")[0].split("/")[0].replace("$", "").replace(",", "")

        rental_data.append({
            "address": address,
            "price": price,
            "link": link
        })

    return rental_data

def save_to_spreadsheet(rental_data: list[dict]):
    credentials = service_account.Credentials.from_service_account_file(
    'cheapest-flight-finder-464513-70046c2a2cc5.json',
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    sheets_service = build('sheets', 'v4', credentials=credentials)
    spreadsheet_id = '1sEEWNviqb7upXzAf9G2dxaOKn94b_GMm6jmM5n9z7Hk'
    sheet_name = 'Sheet1'
    sheet_range = f'{sheet_name}!A2:C'
    for i, rental in enumerate(rental_data):
        values = [
            [rental['address'], rental['price'], rental['link']]
        ]
        body = {
            'values': values
        }
        result = sheets_service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=sheet_range,
            valueInputOption='RAW',
            body=body
        ).execute()
        print(result)
        print(f"Progress: {i+1}/{len(rental_data)}")

rental_data = get_rental_data()
save_to_spreadsheet(rental_data)