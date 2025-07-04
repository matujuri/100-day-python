from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep Chrome browser open after script execution
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# driver.get("https://www.amazon.co.jp/dp/B09S3B1F8H?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1")
# element = driver.find_element(By.CLASS_NAME, "a-price-whole")
# print(element.text)

driver.get("https://www.python.org/")
# search_bar = driver.find_element(By.NAME, "q")
# button = driver.find_element(By.ID, "submit")
# documentation_link = driver.find_element(By.CSS_SELECTOR, ".documentation-widget a")
# bug_link = driver.find_element(By.XPATH, '//*[@id="site-map"]/div[2]/div/ul/li[3]/a')


events = driver.find_elements(By.CSS_SELECTOR, ".event-widget li")
event_dict = {}
for index, event in enumerate(events):
    event_time = event.find_element(By.TAG_NAME, "time").text
    event_name = event.find_element(By.TAG_NAME, "a").text
    event_dict[index] = {
        "time": event_time,
        "name": event_name
    }
print(event_dict)

driver.quit()