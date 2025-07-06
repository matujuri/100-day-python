from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

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
    driver = webdriver.ChromeOptions()
    driver.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=driver)
    data_length = len(rental_data)
    for i, rental in enumerate(rental_data):
        driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdz_XIl2t_8EMQUdegOiNiP8tiJY9qmPVR2knqT18ymkMtWvg/viewform?usp=dialog")
       
        sleep(2)
   
        address = rental["address"]
        price = rental["price"]
        link = rental["link"]
        
        inputs = driver.find_elements(By.CSS_SELECTOR, "input.whsOnd.zHQkBf")
        inputs[0].send_keys(address)
        inputs[1].send_keys(price)
        inputs[2].send_keys(link)
        
        submit_button = driver.find_element(By.XPATH, "//span[contains(text(), '送信')]")
        submit_button.click()
        sleep(1)
        print(f"Progress: {i+1}/{data_length}")

rental_data = get_rental_data()
save_to_spreadsheet(rental_data)
