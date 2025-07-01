class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, depart_date: str, origin: str, destination: str, value: int, is_departure: bool = True, index: int = 0):
        self.depart_date = depart_date
        self.origin = origin
        self.destination = destination
        self.value = value
        self.is_departure = is_departure
        self.index = index # sheet更新用
        
    def __str__(self):
        return f"FlightData(depart_date={self.depart_date}, origin={self.origin}, destination={self.destination}, value={self.value})"