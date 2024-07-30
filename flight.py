#Refer to aircraft clss for comments that explain class structure

import re
from datetime import datetime

class Flight:
    def __init__(self, flightID, flightDate, originAirport, destinationAirport, departureTime, arrivalTime, aircraftID):
        self.flightID = flightID
        self.flightDate = flightDate
        self.originAirport = originAirport
        self.destinationAirport = destinationAirport
        self.departureTime = departureTime
        self.arrivalTime = arrivalTime
        self.aircraftID = aircraftID
        self.validate()

    def validate(self):
        if not isinstance(self.flightID, int):
            raise ValueError("Flight ID must be an integer")
        
        try:
            datetime.strptime(self.flightDate, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Flight date must be in dd/mm/yyyy format")
        
        if not re.match("^[A-Z]{3}$", self.originAirport):
            raise ValueError("Origin airport must be a 3-letter code")
        
        if not re.match("^[A-Z]{3}$", self.destinationAirport):
            raise ValueError("Destination airport must be a 3-letter code")
        
        try:
            datetime.strptime(self.departureTime, "%H:%M:%S")
        except ValueError:
            raise ValueError("Departure time must be in HH:MM:SS format")
        
        try:
            datetime.strptime(self.arrivalTime, "%H:%M:%S")
        except ValueError:
            raise ValueError("Arrival time must be in HH:MM:SS format")

        if not isinstance(self.aircraftID, int):
            raise ValueError("Aircraft ID must be an integer")

    def to_tuple(self):
        return (self.flightID, self.flightDate, self.originAirport, self.destinationAirport, self.departureTime, self.arrivalTime, self.aircraftID)

    def __str__(self):
        return f"Flight(flightID: {self.flightID}, flightDate: {self.flightDate}, originAirport: {self.originAirport}, destinationAirport: {self.destinationAirport}, departureTime: {self.departureTime}, arrivalTime: {self.arrivalTime}, aircraftID: {self.aircraftID})"
