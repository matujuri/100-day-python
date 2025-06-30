#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from flight_search import FlightSearch
from flight_data import FlightData
from data_manager import DataManager

origin = "TYO"

def get_cheapest_flight(origin: str, destination: str):
    flight_search = FlightSearch(origin=origin, destination=destination)
    cheapest_flight = flight_search.get_cheapest_flight_in_a_year()
    if cheapest_flight == {}:
        return
    flight_data = FlightData(
        depart_date=cheapest_flight["depart_date"],
        origin=cheapest_flight["origin"],
        destination=cheapest_flight["destination"],
        value=cheapest_flight["value"]
    )
    return flight_data

data_manager = DataManager()
destination_data = data_manager.get_destination_data()
for destination in destination_data:
    departure_flight_data = get_cheapest_flight(origin, destination)
    if departure_flight_data is not None:
        data_manager.update_price(destination_data.index(destination) + 2, departure_flight_data.value, departure_flight_data.depart_date, True)
    return_flight_data = get_cheapest_flight(destination, origin)
    if return_flight_data is not None:
        data_manager.update_price(destination_data.index(destination) + 2, return_flight_data.value, return_flight_data.depart_date, False)
    