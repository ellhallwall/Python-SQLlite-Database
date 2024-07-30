#Refer to aircraft clss for comments that explain class structure


import re
from datetime import datetime, timedelta

class Pilot:
    def __init__(self, pilotID, first_name, middle_name, last_name, date_of_birth, start_date, license_number):
        self.pilotID = pilotID
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.start_date = start_date
        self.license_number = license_number
        self.validate()

    def validate(self):
        # Validate first_name and last_name
        if not re.match("^[A-Za-z]+$", self.first_name):
            raise ValueError("First name must be characters only.")
        if self.middle_name and not re.match("^[A-Za-z]*$", self.middle_name):
            raise ValueError("Middle name must be characters only or empty.")
        if not re.match("^[A-Za-z]+$", self.last_name):
            raise ValueError("Last name must be characters only.")
        
        # Validate date_of_birth (must be over 18 years old)
        dob = datetime.strptime(self.date_of_birth, "%d/%m/%Y")
        if (datetime.now() - dob).days < 18 * 365:
            raise ValueError("Pilot must be over 18 years old.")

        # Validate start_date (must be in the past or no longer than 1 month into the future)
        start_date = datetime.strptime(self.start_date, "%d/%m/%Y")
        if start_date > datetime.now() + timedelta(days=30):
            raise ValueError("Start date must be in the past or no longer than 1 month into the future.")

        # Validate license_number (must be 8 digits)
        if not re.match("^[0-9]{8}$", str(self.license_number)):
            raise ValueError("License number must be 8 digits.")

    def to_tuple(self):
        return (self.pilotID, self.first_name, self.middle_name, self.last_name, self.date_of_birth, self.start_date, self.license_number)

    def __str__(self):
        return f"Pilot(pilotID: {self.pilotID}, FirstName: {self.first_name}, MiddleName: {self.middle_name}, LastName: {self.last_name}, DateOfBirth: {self.date_of_birth}, StartDate: {self.start_date}, LicenseNumber: {self.license_number})"
