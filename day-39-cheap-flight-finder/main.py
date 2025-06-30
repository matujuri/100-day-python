#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from flight_search import FlightSearch
from flight_data import FlightData
from data_manager import DataManager

origin = "TYO"

def get_lowest_price_and_update_data(origin: str, destination: str, is_departure: bool):
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
    print(flight_data.__str__())
    if is_departure:
        data_manager.update_price(destination_data.index(destination) + 2, flight_data.value, flight_data.depart_date, True)
    else:
        data_manager.update_price(destination_data.index(origin) + 2, flight_data.value, flight_data.depart_date, False)

data_manager = DataManager()
destination_data = data_manager.get_destination_data()
for destination in destination_data:
    get_lowest_price_and_update_data(origin, destination, True)
    get_lowest_price_and_update_data(destination, origin, False)