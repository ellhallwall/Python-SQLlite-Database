#Refer to aircraft clss for comments that explain class structure


class PilotFlight:
    def __init__(self, pilotID, flightID):
        self.pilotID = pilotID
        self.flightID = flightID
        self.validate()

    #validates that pilotID and FlightID are both integers to ensure it accurately
    #represents the many to many relationships
    def validate(self):
        if not isinstance(self.pilotID, int):
            raise ValueError("PilotID must be an integer")
        if not isinstance(self.flightID, int):
            raise ValueError("FlightID must be an integer")

    def to_tuple(self):
        return (self.pilotID, self.flightID)

    def __str__(self):
        return f"PilotFlight(pilotID: {self.pilotID}, flightID: {self.flightID})"
