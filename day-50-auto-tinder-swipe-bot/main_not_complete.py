from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://tinder.com/")

sleep(5)
reject_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., '同意しない')]"))
    )
reject_button.click()
print("cookie reject button clicked")

try:
    # ログインボタンを明示的に待ってからクリック
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'ログイン')]"))
    )
    login_button.click()
    print("login button clicked")
    
    # Google で続けるボタンをクリック
    google_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Google で続ける')]"))
    )
    google_button.click()
    print("google button clicked")
    
except Exception as e:
    print("ログインボタンが見つかりませんでした。", e)
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)  # HTML構造を確認するために出力

