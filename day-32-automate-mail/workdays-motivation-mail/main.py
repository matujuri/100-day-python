import random
import smtplib
from datetime import datetime
from email.message import EmailMessage
import os
import dotenv
dotenv.load_dotenv()

# ---------------------------- LOAD QUOTES ------------------------------- #
FILE_PATH = "day-32-automate-mail/workdays-motivation-mail/quotes.txt"
def quote_of_the_day():
    try:
        with open(FILE_PATH, "r") as file:
            quotes = file.readlines()
    except FileNotFoundError:
        print("File not found")
        quotes = ["No quotes found"]
    else:
        return random.choice(quotes)

# ---------------------------- SEND EMAIL ------------------------------- #
smtp_server = "smtp.gmail.com"
smtp_port = 587
my_email = "b38860114@gmail.com"
password = os.getenv("GMAIL_APP_PASSWORD") #app password

def send_email():
    msg = EmailMessage()
    msg["Subject"] = "やる気の名言"
    msg["From"] = my_email
    msg["To"] = "xiaobaka59@gmail.com"
    msg.set_content(quote_of_the_day(), charset="utf-8")
    
    with smtplib.SMTP(smtp_server, smtp_port) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.send_message(msg)
        print("Email sent successfully")
        
# ---------------------------- Weekly Mail ------------------------------- #

if datetime.now().weekday() < 5:  # 月(0)〜金(4)
    send_email()


