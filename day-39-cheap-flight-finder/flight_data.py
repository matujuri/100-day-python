class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, depart_date: str, origin: str, destination: str, value: int):
        self.depart_date = depart_date
        self.origin = origin
        self.destination = destination
        self.value = value
        
    def __str__(self):
        return f"FlightData(depart_date={self.depart_date}, origin={self.origin}, destination={self.destination}, value={self.value})"