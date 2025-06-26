# ---------------------------- MAIL ------------------------------- #

import smtplib

my_email = "b38860114@gmail.com"
password = "app password"

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email, 
        to_addrs="xiaobaka59@gmail.com", 
        msg="subject:Hello\n\nThis is the body of the email."
    )
    
    
# ---------------------------- TIME ------------------------------- #
from datetime import datetime

now = datetime.now()
print(now)

year = now.year
month = now.month
day = now.day
day_of_week = now.weekday()

print(year, month, day, day_of_week)

date_of_birth = datetime(year=1993, month=2, day=22)
print(date_of_birth)