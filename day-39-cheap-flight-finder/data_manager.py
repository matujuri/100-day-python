import os
import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    SHEETY_ENDPOINT = "https://api.sheety.co/5e9221bf09d3ba652c755231464449ec/cheapFlightFinder/sheet1"
    
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {os.getenv('SHEETY_TOKEN')}"
        }
        
    def write_price_data(self, price_data: list[tuple[str, int, int]]):
        with open("day-39-cheap-flight-finder/price_data.csv", "w") as file:
            file.write("".join([f"{data[0]},{data[1]},{data[2]}\n" for data in price_data]))
    
    def get_destination_data(self)->list[tuple[str, int, int]]:
        csv_data = pd.read_csv("day-39-cheap-flight-finder/price_data.csv")
        destination_data = csv_data[["iataCode"]].values.tolist()
            
        if csv_data.empty:
            response = requests.get(self.SHEETY_ENDPOINT, headers=self.headers)
            response.raise_for_status()
            price_data = [(row["iataCode"], row.get("lowestDeparturePrice", ""), row.get("lowestReturnPrice", "")) for row in response.json()["sheet1"]]
            self.write_price_data(price_data)
            destination_data = [row["iataCode"] for row in response.json()["sheet1"]]
            
        return destination_data
    
    def update_price(self, object_id: int, price: int, depart_date: str, is_departure: bool):
        if is_departure:
            response = requests.put(
                url=f"{self.SHEETY_ENDPOINT}/{object_id}",
                json={"sheet1": {"lowestDeparturePrice": price, "departureDate": depart_date}},
            headers=self.headers
            )
            response.raise_for_status()
        else:
            response = requests.put(
                url=f"{self.SHEETY_ENDPOINT}/{object_id}",
                json={"sheet1": {"lowestReturnPrice": price, "returnDate": depart_date}},
                headers=self.headers
            )
            response.raise_for_status()