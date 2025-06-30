import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    TRAVELPAYOUTS_API_KEY = os.getenv("TRAVELPAYOUTS_API_KEY")
    TRAVELPAYOUTS_CURRENCY = "JPY"
    FLIGHT_SEARCH_ENDPOINT = "https://api.travelpayouts.com/v2/prices/latest"
    
    def __init__(self, origin: str, destination: str):
        self.headers = {
            "X-Access-Token": self.TRAVELPAYOUTS_API_KEY
        }
        self.origin = origin
        self.destination = destination
        self.params = {
            "origin": self.origin,
            "destination": self.destination,
            "currency": self.TRAVELPAYOUTS_CURRENCY,
            "limit": 1,
            "period_type": "year",
            "one_way": True
        }

    def get_cheapest_flight_in_a_year(self) -> dict:
        response = requests.get(self.FLIGHT_SEARCH_ENDPOINT, params=self.params, headers=self.headers)
        response.raise_for_status()
        return response.json()["data"][0]