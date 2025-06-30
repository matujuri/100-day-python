import os
import smtplib
from flight_data import FlightData

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USERNAME = os.getenv("GMAIL_USERNAME")
    SMTP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
    SMTP_FROM = os.getenv("GMAIL_USERNAME")
    
    def __init__(self, to_addrs: str):
        self.to_addrs = to_addrs
        
    def send_email(self, flight_data: FlightData):
        with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as connection:
            connection.starttls()
            connection.login(user=self.SMTP_USERNAME, password=self.SMTP_PASSWORD)
            connection.sendmail(
                from_addr=self.SMTP_FROM,
                to_addrs=self.to_addrs,
                msg=f"Subject: Flight Lowest Price Alert!\n\nOnly {flight_data.value} JPY to fly from {flight_data.origin} to {flight_data.destination} on {flight_data.depart_date}"
            )

        