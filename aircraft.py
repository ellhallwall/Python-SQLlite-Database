import re #modules for srting validation
from datetime import datetime #modules for date validation

class Aircraft:
    #Attributes of the aircraft table
    def __init__(self, aircraftID, manufacturer, model, capacity, purchase_date, maintenance_date):
        self.aircraftID = aircraftID
        self.manufacturer = manufacturer
        self.model = model
        self.capacity = capacity
        self.purchase_date = purchase_date
        self.maintenance_date = maintenance_date
        self.validate()

    def validate(self):
        # Validate manufacturer and model - can be alphanumeric
        if not re.match("^[A-Za-z0-9]+$", self.manufacturer):
            raise ValueError("Manufacturer must be alphanumeric.")
        if not re.match("^[A-Za-z0-9]+$", self.model):
            raise ValueError("Model must be alphanumeric.")

        # Validate capacity - must be a number
        if not isinstance(self.capacity, int) or self.capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")

        # Validate dates - must be in dd/mm/yyyy format
        try:
            datetime.strptime(self.purchase_date, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Purchase date must be in dd/mm/yyyy format.")
        try:
            datetime.strptime(self.maintenance_date, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Maintenance date must be in dd/mm/yyyy format.")

    #Convert to tuple so can be inserted into DB
    def to_tuple(self):
        return (self.aircraftID, self.manufacturer, self.model, self.capacity, self.purchase_date, self.maintenance_date)

    #Returns string which can be used for printing
    def __str__(self):
        return f"Aircraft(AircraftID: {self.aircraftID}, Manufacturer: {self.manufacturer}, Model: {self.model}, Capacity: {self.capacity}, PurchaseDate: {self.purchase_date}, MaintenanceDate: {self.maintenance_date})"
