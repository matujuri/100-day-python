from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from dotenv import load_dotenv
import os
import traceback

load_dotenv()

USERNAME = os.getenv("username")
PASSWORD = os.getenv("password")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.linkedin.com/jobs/search/?currentJobId=4210573994&f_AL=true&f_WT=2&geoId=101355337&keywords=ux%20designer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true")

try:
    # ページが完全にロードされるまで待機 (JavaScriptの実行も含む)
    WebDriverWait(driver, 15).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    print("ページロード完了。")

    # 要素が存在するまで待機（クリック可能かどうかは問わない）
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sign-in-modal__outlet-btn"))
    )
    # JavaScriptを実行して要素をクリック
    driver.execute_script("arguments[0].click();", sign_in_button)
    print("Sign-in buttonがJavaScriptでクリックされました。")
    
    # クリック後の状態を確認するために少し待機
    sleep(3) 

    # ログインモーダルが表示されるのを待機
    print("ログインモーダルが表示されるのを待機します...")
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "session_key"))
    )
    print("ログインモーダルが表示されました。")

    print("JavaScriptを使ってユーザー名を入力します。")
    # JavaScriptを使ってユーザー名フィールドの値を直接設定
    driver.execute_script("arguments[0].value = arguments[1];", username_field, USERNAME)
    
    print("JavaScriptを使ってパスワードを入力します。")
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "session_password"))
    )
    # JavaScriptを使ってパスワードフィールドの値を直接設定
    driver.execute_script("arguments[0].value = arguments[1];", password_field, PASSWORD)
    
    print("最終的なサインインボタンを探し、JavaScriptを使ってクリックします。")
    final_sign_in_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-primary.sign-in-form__submit-btn--full-width"))
    )
    driver.execute_script("arguments[0].click();", final_sign_in_button)
    print("最終的なサインインボタンがJavaScriptでクリックされました。")
    
    sleep(5) 

    print("ログインプロセスが完了しました。")
    
    driver.get("https://www.linkedin.com/jobs/search/?distance=25&f_AL=true&f_WT=2&geoId=101355337&keywords=ux%20designer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true")
    print("仕事一覧を表示しました。")
    
    sleep(5) 
    
    job_list = driver.find_elements(By.CLASS_NAME, 'job-card-list__title--link')
    for job in job_list:
        job.click()
        print("job clicked")
        sleep(5)
        apply_button = driver.find_element(By.CLASS_NAME, 'jobs-save-button')
        apply_button.click()
        print("apply button clicked")
        sleep(5)

except Exception as e:
    print(f"エラーが発生しました: {e}")
    # より詳細なエラー情報を表示
    print("--- 完全なトレースバック ---")
    traceback.print_exc()
    print("----------------------------")

