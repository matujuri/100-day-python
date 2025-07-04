from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# driver.get("https://en.wikipedia.org/wiki/Main_Page")
# article_count = driver.find_element(By.XPATH, '//*[@id="articlecount"]/ul/li[2]/a[1]')   
# article_count.click()

# all_portals = driver.find_element(By.LINK_TEXT, "Content portals")
# all_portals.click()

# search = driver.find_element(By.NAME, "search")
# search.send_keys("Python", Keys.ENTER)

driver.get("https://secure-retreat-92358.herokuapp.com/")
first_name = driver.find_element(By.NAME, "fName") 
first_name.send_keys("John")

last_name = driver.find_element(By.NAME, "lName")
last_name.send_keys("Doe")

email = driver.find_element(By.NAME, "email")
email.send_keys("john.doe@example.com")

submit = driver.find_element(By.TAG_NAME, "button")
submit.click()

# driver.quit()