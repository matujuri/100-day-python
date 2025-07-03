import requests
from bs4 import BeautifulSoup
from notification_manager import NotificationManager
import os
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = os.getenv("USER_AGENT")
ACCEPT_LANGUAGE = os.getenv("ACCEPT_LANGUAGE")
URL = "https://appbrewery.github.io/instant_pot/"
PRICE_THRESHOLD = 100

HEADERS = {
    "Accept-Language": ACCEPT_LANGUAGE, 
    "User-Agent": USER_AGENT
}

response = requests.get(URL, headers=HEADERS)

soup = BeautifulSoup(response.text, "html.parser")

price_whole = soup.find(name="span", class_="a-price-whole")
price_fraction = soup.find(name="span", class_="a-price-fraction")
print(price_whole.getText() + price_fraction.getText())

notification_manager = NotificationManager()
# send email if price is less than 100
if float(price_whole.getText() + price_fraction.getText()) < PRICE_THRESHOLD:
    notification_manager.send_email(
        to_addrs="xiaobaka59@gmail.com",
        subject="Amazon Price Alert!",
        message=f"The price of the product is now {price_whole.getText() + price_fraction.getText()}"
    )








