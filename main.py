import sqlite3
import re
from db_operations import DBOperations
from pilot import Pilot
from aircraft import Aircraft
from flight import Flight
from pilot_flight import PilotFlight

#Checks the list of tables names to ensure they are created by looping over the list
#If tables are not there, it will prompt the user to create them via the option below
def tables_exist(db_ops):
    tables = ['Aircraft', 'Pilot', 'Flight', 'PilotFlight']
    db_ops.get_connection()  
    for table in tables:
        try:
            db_ops.check_table_exists(table)
        except ValueError:
            db_ops.close_connection()  
            return False
    db_ops.close_connection()  
    return True

def main():
    db_ops = DBOperations()

    while True:
        print("\nMenu:")
        print("0. Exit")
        print("1. Create Tables")
        print("2. Drop Tables")
        print("3. Insert Record")
        print("4. View All Records")
        print("5. Update Record")
        print("6. Delete Record")
        print("7. Search Records")
        print("8. Search All Attributes")
        print("9. Total Number of Flights")
        print("10. Number of Flights Per Aircraft")
        print("11. Total Number of Pilots")
        print("12. Count Tables")

        choice = input("Enter your choice: ")

        #Cycles through various methods outlines in db_operations
        if choice == "1":
            db_ops.create_tables()
        elif choice == "2":
            db_ops.drop_tables()
        elif choice == "3":
            if not tables_exist(db_ops):
                print("Tables do not exist. Please create tables first.")
                continue
            table_name = input("Enter the table name (Aircraft, Pilot, Flight, PilotFlight): ")
            if table_name == "Pilot":
                while True:
                    try:
                        pilotID = int(input("Enter pilot ID: "))
                        first_name = input("Enter first name: ")
                        middle_name = input("Enter middle name (or press Enter to leave empty): ")
                        last_name = input("Enter last name: ")
                        date_of_birth = input("Enter date of birth (dd/mm/yyyy): ")
                        start_date = input("Enter start date (dd/mm/yyyy): ")
                        license_number = int(input("Enter license number (8 digits): "))
                        pilot = Pilot(pilotID, first_name, middle_name, last_name, date_of_birth, start_date, license_number)
                        db_ops.insert_record('Pilot', pilot)
                        break
                    except ValueError as e:
                        print(f"Validation error: {e}")
                    except sqlite3.Error as e:
                        print(f"Database error: {e}")
            elif table_name == "Aircraft":
                while True:
                    try:
                        aircraftID = int(input("Enter aircraft ID: "))
                        manufacturer = input("Enter manufacturer: ")
                        model = input("Enter model: ")
                        capacity = int(input("Enter capacity: "))
                        purchase_date = input("Enter purchase date (dd/mm/yyyy): ")
                        maintenance_date = input("Enter maintenance date (dd/mm/yyyy): ")
                        aircraft = Aircraft(aircraftID, manufacturer, model, capacity, purchase_date, maintenance_date)
                        db_ops.insert_record('Aircraft', aircraft)
                        break
                    except ValueError as e:
                        print(f"Validation error: {e}")
                    except sqlite3.Error as e:
                        print(f"Database error: {e}")
            elif table_name == "Flight":
                while True:
                    try:
                        flightID = int(input("Enter flight ID: "))
                        flightDate = input("Enter flight date (dd/mm/yyyy): ")
                        originAirport = input("Enter origin airport (3-letter code): ")
                        destinationAirport = input("Enter destination airport (3-letter code): ")
                        departureTime = input("Enter departure time (HH:MM:SS): ")
                        arrivalTime = input("Enter arrival time (HH:MM:SS): ")
                        aircraftID = int(input("Enter aircraft ID: "))  # Add aircraftID to Flight
                        flight = Flight(flightID, flightDate, originAirport, destinationAirport, departureTime, arrivalTime, aircraftID)
                        db_ops.insert_record('Flight', flight)
                        break
                    except ValueError as e:
                        print(f"Validation error: {e}")
                    except sqlite3.Error as e:
                        print(f"Database error: {e}")
            elif table_name == "PilotFlight":
                while True:
                    try:
                        pilotID = int(input("Enter pilot ID: "))
                        flightID = int(input("Enter flight ID: "))
                        pilot_flight = PilotFlight(pilotID, flightID)
                        db_ops.insert_record('PilotFlight', pilot_flight)
                        break
                    except ValueError as e:
                        print(f"Validation error: {e}")
                    except sqlite3.Error as e:
                        print(f"Database error: {e}")
            else:
                print("Invalid table name.")
        elif choice == "4":
            if not tables_exist(db_ops):
                print("Tables do not exist. Please create tables first.")
                continue
            try:
                table_name = input("Enter the table name (Aircraft, Pilot, Flight, PilotFlight): ")
                db_ops.select_all_records(table_name)
            except ValueError as e:
                print(f"Error: {e}")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        elif choice == "5":
            if not tables_exist(db_ops):
                print("Tables do not exist. Please create tables first.")
                continue
            try:
                table_name = input("Enter the table name (Aircraft, Pilot, Flight, PilotFlight): ")
                condition_column = input("Name of ID column: ")
                condition_value = input("ID of record you want to change: ")
                update_column = input("Which column would you like to change? (Please type the column header): ")
                new_value = input("New value: ")
                db_ops.update_record(table_name, condition_column, condition_value, [update_column], [new_value])
            except ValueError as e:
                print(f"Error: {e}")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        elif choice == "6":
            if not tables_exist(db_ops):
                print("Tables do not exist. Please create tables first.")
                continue
            try:
                table_name = input("Enter the table name (Aircraft, Pilot, Flight, PilotFlight): ")
                condition_column = input("Enter the condition column (column to match for the deletion): ")
                condition_value = input("Enter the condition value (value to match in the condition column): ")
                db_ops.delete_record(table_name, condition_column, condition_value)
            except ValueError as e:
                print(f"Error: {e}")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        elif choice == "7":
            if not tables_exist(db_ops):
                print("Tables do not exist. Please create tables first.")
                continue
            try:
                table_name = input("Enter the table name (Aircraft, Pilot, Flight, PilotFlight): ")
                attribute = input("Enter the attribute to search by: ")
                value = input("Enter the value to search for: ")
                db_ops.search(table_name, attribute, value)
            except ValueError as e:
                print(f"Error: {e}")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        elif choice == "8":
            if not tables_exist(db_ops):
                print("Tables do not exist. Please create tables first.")
                continue
            try:
                table_name = input("Enter the table name (Aircraft, Pilot, Flight, PilotFlight): ")
                search_value = input("Enter the search value: ")
                db_ops.search_all_attributes(table_name, search_value)
            except ValueError as e:
                print(f"Error: {e}")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        elif choice == "9":
            if not tables_exist(db_ops):
                print("Tables do not exist. Please create tables first.")
                continue
            try:
                db_ops.total_number_of_flights()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        elif choice == "10":
            if not tables_exist(db_ops):
                print("Tables do not exist. Please create tables first.")
                continue
            try:
                db_ops.number_of_flights_per_aircraft()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        elif choice == "11":
            if not tables_exist(db_ops):
                print("Tables do not exist. Please create tables first.")
                continue
            try:
                db_ops.total_number_of_pilots()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        elif choice == "12":
            try:
                db_ops.count_tables()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
