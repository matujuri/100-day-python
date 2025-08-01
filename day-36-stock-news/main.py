import requests
import os
import dotenv
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
dotenv.load_dotenv()

STOCK = "AMZN"
COMPANY_NAME = "Amazon Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

def get_stock_data(stock_symbol) -> list:
    alphavantage_parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_symbol,
        "apikey": os.getenv("ALPHAVANTAGE_API_KEY")
    }
    
    response = requests.get(STOCK_ENDPOINT, params=alphavantage_parameters)
    response.raise_for_status()
    data = response.json()
    daily_data = data["Time Series (Daily)"]
    return list(daily_data.values())

# indexの0は最新の日付、1は一日前の日付
def get_closing_price(stock_data, index) -> float:
    return float(stock_data[index]["4. close"])
    
def get_percentage_change(stock_data) -> float:
    yesterday_closing_price = get_closing_price(stock_data, 0)
    day_before_yesterday_closing_price = get_closing_price(stock_data, 1)
    return round(((yesterday_closing_price - day_before_yesterday_closing_price) / day_before_yesterday_closing_price) * 100, 2)

def get_change_emoji(percentage_change) -> str:
    if percentage_change > 5:
        return "🔺"
    else:
        return "🔻"

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

def get_news(company_name: str) -> list:
    day_before_yesterday = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")

    newsapi_parameters = {
        "q": company_name,
        "sortBy": "popularity",
        "searchIn": "title,description",
        "from": day_before_yesterday,
        "apiKey": os.getenv("NEWS_API_KEY")
    }

    response = requests.get(NEWS_ENDPOINT, params=newsapi_parameters)
    response.raise_for_status()
    data = response.json()  

    return data["articles"][:3]

def get_news_content(articles: list):
    return "".join([f"Headline: {article['title']}\nBrief: {article['description']}\npublishedAt: {article['publishedAt']}\nurl: {article['url']}\n" for article in articles])

## STEP 3: send mail
def send_mail(news_content: str, change_emoji: str, percentage_change: float):
    # メールの件名と本文を作成します。
    subject = f"{COMPANY_NAME}: {change_emoji}{percentage_change}%"
    body = f"{news_content}"
    
    # MIMETextオブジェクトを作成し、UTF-8でエンコードします。
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = os.getenv("FROM_EMAIL")
    msg['To'] = os.getenv("TO_EMAIL")

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=os.getenv("FROM_EMAIL"), password=os.getenv("GMAIL_APP_PASSWORD"))
        connection.send_message(msg)
        print("Mail sent")

def main():
    stock_data = get_stock_data(STOCK)
    percentage_change = get_percentage_change(stock_data)

    if percentage_change > 5 or percentage_change < -5:
        change_emoji = get_change_emoji(percentage_change)
        news = get_news(COMPANY_NAME)
        news_content = get_news_content(news)
        send_mail(news_content, change_emoji, percentage_change)
    else:
        print("No news")
        change_emoji = get_change_emoji(percentage_change)
        news = get_news(COMPANY_NAME)
        news_content = get_news_content(news)
        send_mail(news_content, change_emoji, percentage_change)
        
main()
