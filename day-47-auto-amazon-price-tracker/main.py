import requests
from bs4 import BeautifulSoup
from notification_manager import NotificationManager
import os
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = os.getenv("USER_AGENT")
ACCEPT_LANGUAGE = os.getenv("ACCEPT_LANGUAGE")
URL = "https://www.amazon.co.jp/dp/B09S3B1F8H?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1"
PRICE_THRESHOLD = 3900

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
    "Accept-Encoding": "gzip, deflate, br, zstd", 
    "Accept-Language": ACCEPT_LANGUAGE, 
    "Priority": "u=0, i", 
    "Sec-Ch-Ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"", 
    "Sec-Ch-Ua-Mobile": "?0", 
    "Sec-Ch-Ua-Platform": "\"macOS\"", 
    "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate", 
    "Sec-Fetch-Site": "cross-site", 
    "Sec-Fetch-User": "?1", 
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": USER_AGENT, 
}

response = requests.get(URL, headers=HEADERS)

soup = BeautifulSoup(response.text, "html.parser")
price_whole = soup.find(name="span", class_="a-price-whole")
price=price_whole.getText().replace(",", "")

notification_manager = NotificationManager()
# send email if price is less than 100
if int(price) < PRICE_THRESHOLD:
    notification_manager.send_email(
        to_addrs="xiaobaka59@gmail.com",
        subject="Amazon Price Alert!",
        message=f"The price of the product is now {price}"
    )








