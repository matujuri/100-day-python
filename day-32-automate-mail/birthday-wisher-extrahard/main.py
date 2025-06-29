##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.

import pandas as pd
from datetime import datetime
import random
import smtplib

# ---------------------------- LOAD BIRTHDAYS ------------------------------- #
def birthday_person(date):
    try:
        birthdays = pd.read_csv("birthdays.csv")
        birthdays_dict = birthdays.to_dict(orient="records")
        birthday_person = [birthday for birthday in birthdays_dict if birthday["month"] == date.month and birthday["day"] == date.day]
        return birthday_person
    except FileNotFoundError:
        print("No birthdays found")
        return []

# ---------------------------- LOAD LETTER TEMPLATES ------------------------------- #
def load_letter_template():
    with open(f"letter_templates/letter_{random.randint(1, 3)}.txt", "r") as file:
        letter = file.read()
    return letter

# ---------------------------- SEND EMAIL ------------------------------- #
smtp_server = "smtp.gmail.com"
smtp_port = 587
my_email = "b38860114@gmail.com"
password = "qrsn fyzq nsdp ufln" #app password

def send_email(content, email):
    with smtplib.SMTP(smtp_server, smtp_port) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email, 
            to_addrs=email, 
            msg=f"subject:Happy Birthday!\n\n{content}"
        )
        print("Email sent successfully")
        
# ---------------------------- MAIN ------------------------------- #
today = datetime.now()
birthday_person = birthday_person(today)
if len(birthday_person) > 0:
    for person in birthday_person:
        letter_template = load_letter_template()
        content = letter_template.replace("[NAME]", person["name"])
        send_email(content, person["email"])
else:
    print("No birthdays found")



