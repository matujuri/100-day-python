#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from flight_search import FlightSearch

origin = "TYO"
destination = "SHA"

flight_search = FlightSearch(origin=origin, destination=destination)
cheapest_flight = flight_search.get_cheapest_flight_in_six_months()
print(cheapest_flight)