#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from flight_search import FlightSearch
from flight_data import FlightData
from data_manager import DataManager

origin = "TYO"
destination = ""

data_manager = DataManager()
destination_data = data_manager.get_destination_data()
for destination in destination_data:
    flight_search = FlightSearch(origin=origin, destination=destination)
    cheapest_flight = flight_search.get_cheapest_flight_in_six_months()
    flight_data = FlightData(
        depart_date=cheapest_flight["depart_date"],
        origin=cheapest_flight["origin"],
        destination=cheapest_flight["destination"],
        value=cheapest_flight["value"]
    )
    print(flight_data.__str__())