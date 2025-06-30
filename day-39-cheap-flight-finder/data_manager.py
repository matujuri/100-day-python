import os
import requests
from dotenv import load_dotenv

load_dotenv()

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    SHEETY_ENDPOINT = "https://api.sheety.co/5e9221bf09d3ba652c755231464449ec/cheapFlightFinder/sheet1"
    
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {os.getenv('SHEETY_TOKEN')}"
        }
    
    
    def get_destination_data(self)->list[str]:
        with open("day-39-cheap-flight-finder/destination_data.txt", "r") as file:
            destination_data = file.read().split(",")
            
        if destination_data == ['']:
            response = requests.get(self.SHEETY_ENDPOINT, headers=self.headers)
            response.raise_for_status()
            destination_data = [row["iataCode"] for row in response.json()["sheet1"]]
            with open("day-39-cheap-flight-finder/destination_data.txt", "w") as file:
                file.write(",".join(destination_data))
        
        return destination_data
    
    