import requests
from datetime import datetime
import time
import smtplib
import os
import dotenv
dotenv.load_dotenv()

MY_LAT = 35.443707
MY_LNG = 139.638031
MY_EMAIL = "b38860114@gmail.com"
MY_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def is_iss_overhead():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()["iss_position"]
    latitude = data["latitude"]
    longitude = data["longitude"]
    
    if MY_LAT - 5 <= float(latitude) <= MY_LAT + 5 and MY_LNG - 5 <= float(longitude) <= MY_LNG + 5:
        return True
    else:
        return False

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]
    sunrise_hour = int(datetime.fromisoformat(sunrise).hour)
    sunset_hour = int(datetime.fromisoformat(sunset).hour)

    time_now = datetime.now().hour
    # it is night if the time is between sunset and sunrise
    if time_now >= sunset_hour or time_now <= sunrise_hour:
        return True
    else:
        return False


while True:
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="xiaobaka59@gmail.com",
                msg="Subject:Look up!\n\nThe ISS is above you in the sky."
            )   
    time.sleep(60)