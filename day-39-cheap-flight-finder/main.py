#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from flight_search import FlightSearch
from flight_data import FlightData
from data_manager import DataManager
from notification_manager import NotificationManager
import os
import dotenv
dotenv.load_dotenv()

origin = "TYO"
to_addrs = os.getenv("TO_ADDRS")

def get_cheapest_flight(origin: str, destination: str):
    flight_search = FlightSearch(origin=origin, destination=destination)
    cheapest_flight = flight_search.get_cheapest_flight_in_a_year()
    if cheapest_flight == {}:
        return None
    flight_data = FlightData(
        depart_date=cheapest_flight["depart_date"],
        origin=cheapest_flight["origin"],
        destination=cheapest_flight["destination"],
        value=cheapest_flight["value"]
    )
    print(flight_data.__str__())
    return flight_data

data_manager = DataManager()
destination_data = data_manager.get_destination_data()
notification_manager = NotificationManager(to_addrs=to_addrs)

for destination in destination_data:
    departure_flight_data = get_cheapest_flight(origin, destination)
    price_data = data_manager.get_price_data(destination)
    if departure_flight_data is not None and (price_data[0] == 0 or departure_flight_data.value < price_data[0] - 1000):
        data_manager.update_price(destination_data.index(destination), departure_flight_data.value, departure_flight_data.depart_date, True)
        print(f"Updated departure price for {destination} from {price_data[0]} to {departure_flight_data.value}")
        if departure_flight_data.value < price_data[0] - 1000:
            notification_manager.send_email(departure_flight_data)
            print(f"Sent email for {destination} from {price_data[0]} to {departure_flight_data.value}")
    
    return_flight_data = get_cheapest_flight(destination, origin)
    if return_flight_data is not None and (price_data[1] == 0 or return_flight_data.value < price_data[1] - 1000):
        data_manager.update_price(destination_data.index(destination), return_flight_data.value, return_flight_data.depart_date, False)
        print(f"Updated return price for {destination} from {price_data[1]} to {return_flight_data.value}")
        if return_flight_data.value < price_data[1] - 1000:
            notification_manager.send_email(return_flight_data)
            print(f"Sent email for {destination} from {price_data[1]} to {return_flight_data.value}")