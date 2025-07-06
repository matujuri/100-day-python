from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
from dotenv import load_dotenv
load_dotenv()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)


def get_net_speed():
    driver.get("https://www.speedtest.net/ja")

    go_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Go')]"))
    )
    go_button.click()
    
    sleep(60)
    
    download_speed = driver.find_element(By.CLASS_NAME, "download-speed")
    print(download_speed.text)
    
    upload_speed = driver.find_element(By.CLASS_NAME, "upload-speed")
    print(upload_speed.text)

def login_to_twitter(): 
    driver.get("https://x.com/i/flow/login")

    email_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@autocomplete='username']"))
    )
    email_input.send_keys(os.getenv("TWITTER_USERNAME"))
    print("email inputted")

    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '次へ')]"))
    )
    next_button.click()
    print("next button clicked")

    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@autocomplete='current-password']"))
    )
    password_input.send_keys(os.getenv("TWITTER_PASSWORD"))
    print("password inputted")

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'ログイン')]"))
    )
    login_button.click()
    print("login button clicked")



get_net_speed()