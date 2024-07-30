import sqlite3
import re

class DBOperations:
    #Initialise DB
    def __init__(self, db_name="airline.db"):
        self.db_name = db_name
        self.conn = None
        self.cur = None

    #Connection management
    #Establishes connection to DB
    def get_connection(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
    #Closes the connection to dB
    def close_connection(self):
        if self.conn:
            self.conn.close()

    #Table management
    #Creates the initial tables
    def create_tables(self):
        try:
            self.get_connection()
            create_aircraft_table = """
            CREATE TABLE IF NOT EXISTS Aircraft (
                AircraftID INTEGER PRIMARY KEY,
                Manufacturer TEXT,
                Model TEXT,
                Capacity INTEGER,
                PurchaseDate TEXT,
                MaintenanceDate TEXT
            );
            """
            create_pilot_table = """
            CREATE TABLE IF NOT EXISTS Pilot (
                PilotID INTEGER PRIMARY KEY,
                FirstName TEXT,
                MiddleName TEXT,
                LastName TEXT,
                DateOfBirth TEXT,
                StartDate TEXT,
                LicenseNumber INTEGER
            );
            """
            create_flight_table = """
            CREATE TABLE IF NOT EXISTS Flight (
                FlightID INTEGER PRIMARY KEY,
                FlightDate TEXT,
                OriginAirport TEXT,
                DestinationAirport TEXT,
                DepartureTime TEXT,
                ArrivalTime TEXT,
                AircraftID INTEGER,
                FOREIGN KEY (AircraftID) REFERENCES Aircraft(AircraftID)
            );
            """
            create_pilotflight_table = """
            CREATE TABLE IF NOT EXISTS PilotFlight (
                PilotID INTEGER,
                FlightID INTEGER,
                PRIMARY KEY (PilotID, FlightID),
                FOREIGN KEY (PilotID) REFERENCES Pilot(PilotID),
                FOREIGN KEY (FlightID) REFERENCES Flight(FlightID)
            );
            """
            self.cur.execute(create_aircraft_table)
            self.cur.execute(create_pilot_table)
            self.cur.execute(create_flight_table)
            self.cur.execute(create_pilotflight_table)
            self.conn.commit()
            print("Tables created successfully")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
        finally:
            self.close_connection()

    #Drops/Deletes the tables from the DB
    def drop_tables(self):
        try:
            self.get_connection()
            drop_aircraft_table = "DROP TABLE IF EXISTS Aircraft;"
            drop_pilot_table = "DROP TABLE IF EXISTS Pilot;"
            drop_flight_table = "DROP TABLE IF EXISTS Flight;"
            drop_pilotflight_table = "DROP TABLE IF EXISTS PilotFlight;"
            
            self.cur.execute(drop_aircraft_table)
            self.cur.execute(drop_pilot_table)
            self.cur.execute(drop_flight_table)
            self.cur.execute(drop_pilotflight_table)
            self.conn.commit()
            print("Tables dropped successfully")
        except sqlite3.Error as e:
            print(f"Error dropping tables: {e}")
        finally:
            self.close_connection()

    #Checks if a table exists, helps to avoid errors when performing CRUD operations
    def check_table_exists(self, table_name):
        try:
            self.cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            if not self.cur.fetchone():
                raise ValueError(f"Table {table_name} does not exist.")
        except sqlite3.Error as e:
            print(f"Error checking if table exists: {e}")
    
    #Gets the column names from table
    def get_table_columns(self, table_name):
        try:
            self.cur.execute(f"PRAGMA table_info({table_name})")
            columns = [info[1] for info in self.cur.fetchall()]
            return columns
        except sqlite3.Error as e:
            print(f"Error getting columns for table {table_name}: {e}")
            return []

    #counts number of tables created
    def count_tables(self):
        try:
            self.get_connection()
            self.cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table';")
            table_count = self.cur.fetchone()[0]
            print("Total number of tables:", table_count)
        except sqlite3.Error as e:
            print(f"Error counting tables: {e}")
        finally:
            self.close_connection()

    # CRUD operations
    #Enables user to insert a record into any table, by using a try block and checking the DB connection 
    #and whether the table exists, before joining the strings and converting into a tuple before inserting
    #I validate the ID's for the junction table PilotFLight
    def insert_record(self, table_name, obj):
        try:
            self.get_connection()  
            self.check_table_exists(table_name)
            columns = self.get_table_columns(table_name)
            if not columns:
                raise ValueError(f"Cannot retrieve columns for table {table_name}.")
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['?'] * len(columns))
            values = obj.to_tuple()
            
            # Validation for PilotFlight relationships for junction table
            if table_name == 'PilotFlight':
                if not self.record_exists('Pilot', 'PilotID', obj.pilotID):
                    raise ValueError(f"PilotID {obj.pilotID} does not exist in Pilot table.")
                if not self.record_exists('Flight', 'FlightID', obj.flightID):
                    raise ValueError(f"FlightID {obj.flightID} does not exist in Flight table.")

            insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});"
            
            self.cur.execute(insert_sql, values)
            self.conn.commit()
            print(f"Inserted record into {table_name} successfully")
        except sqlite3.Error as e:
            print(f"Error inserting record into {table_name}: {e}")
        finally:
            self.close_connection()  # Close connection after inserting record

    #Selects all records from a table and prints to the terminal
    def select_all_records(self, table_name):
        try:
            self.get_connection()
            self.check_table_exists(table_name)
            select_all_sql = f"SELECT * FROM {table_name};"
            self.cur.execute(select_all_sql)
            records = self.cur.fetchall()
            for record in records:
                print(record)
        except sqlite3.Error as e:
            print(f"Error selecting all records from {table_name}: {e}")
        finally:
            self.close_connection()

    #Uses a try block to check for a DB connection and table, before preparing SQL statement
    # to combine update values and the condition value I.E the identifier of the record to be updated
    def update_record(self, table_name, condition_column, condition_value, update_columns, update_values):
        try:
            self.get_connection()  
            self.check_table_exists(table_name)

            set_clause = ', '.join([f"{col.strip()} = ?" for col in update_columns])
            update_sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition_column} = ?;"
            
            # Combine update values and condition value into one list
            values = update_values + [condition_value]

            self.cur.execute(update_sql, values)
            self.conn.commit()

            if self.cur.rowcount != 0:
                print(f"{self.cur.rowcount} Row(s) updated.")
            else:
                print(f"Cannot find this record in the {table_name} table.")
        except sqlite3.Error as e:
            print(f"Error updating record in {table_name}: {e}")
        finally:
            self.close_connection() 

    #Enables the user to delete a record from a table
    def delete_record(self, table_name, condition_column, condition_value):
        try:
            self.get_connection()
            self.check_table_exists(table_name)
            delete_sql = f"DELETE FROM {table_name} WHERE {condition_column} = ?;"
            self.cur.execute(delete_sql, (condition_value,))
            self.conn.commit()
            if self.cur.rowcount != 0:
                print(f"{self.cur.rowcount} Row(s) deleted.")
            else:
                print(f"Cannot find this record in the {table_name} table")
        except sqlite3.Error as e:
            print(f"Error deleting record from {table_name}: {e}")
        finally:
            self.close_connection()

    #Allows users to search for a record in a table by using a try block to check the DB connection
    #the SQL statement uses a select, where to find an attribute before fetching and printing results
    def search(self, table_name, attribute, value):
        try:
            self.get_connection()
            self.check_table_exists(table_name)
            search_sql = f"SELECT * FROM {table_name} WHERE {attribute} = ?;"
            self.cur.execute(search_sql, (value,))
            results = self.cur.fetchall()
            for result in results:
                print(result)
            if not results:
                print(f"No results found for {attribute} = {value} in {table_name}.")
        except sqlite3.Error as e:
            print(f"Error searching records in {table_name}: {e}")
        finally:
            self.close_connection()

    #This method uses a similar apprroach, but instead of where it uses a 'Like' condition
    #This enables the user to search for more general information, whereas the previous method 
    #Requires a more specific search
    def search_all_attributes(self, table_name, search_value):
        try:
            self.get_connection()
            self.check_table_exists(table_name)
            columns = self.get_table_columns(table_name)
            if not columns:
                raise ValueError(f"Cannot retrieve columns for table {table_name}.")
            search_conditions = ' OR '.join([f"{col} LIKE ?" for col in columns])
            search_sql = f"SELECT * FROM {table_name} WHERE {search_conditions}"
            search_values = [f"%{search_value}%"] * len(columns)
            self.cur.execute(search_sql, search_values)
            results = self.cur.fetchall()
            for result in results:
                print(result)
        except sqlite3.Error as e:
            print(f"Error searching all attributes in {table_name}: {e}")
        finally:
            self.close_connection()

    #Checks if a record exists, similar to the check_table_exists method. This helps to avoid errors when performing CRUD operations
    def record_exists(self, table_name, column_name, value):
        try:
            self.cur.execute(f"SELECT 1 FROM {table_name} WHERE {column_name} = ? LIMIT 1;", (value,))
            exists = self.cur.fetchone() is not None
            return exists
        except sqlite3.Error as e:
            print(f"Error checking if record exists: {e}")
            return False

    #Statistics on the database
    def total_number_of_flights(self):
        try:
            self.get_connection()
            self.check_table_exists('Flight')
            total_flights_sql = "SELECT COUNT(*) FROM Flight;"
            self.cur.execute(total_flights_sql)
            total_flights = self.cur.fetchone()[0]
            print("Total number of flights:", total_flights)
        except sqlite3.Error as e:
            print(f"Error getting total number of flights: {e}")
        finally:
            self.close_connection()

    def number_of_flights_per_aircraft(self):
        try:
            self.get_connection()
            self.check_table_exists('Flight')
            flights_per_aircraft_sql = """
            SELECT Aircraft.AircraftID, COUNT(*) as FlightCount
            FROM Flight
            JOIN Aircraft ON Flight.AircraftID = Aircraft.AircraftID
            GROUP BY Aircraft.AircraftID;
            """
            self.cur.execute(flights_per_aircraft_sql)
            flights_per_aircraft = self.cur.fetchall()
            for row in flights_per_aircraft:
                print(f"AircraftID: {row[0]}, Number of Flights: {row[1]}")
        except sqlite3.Error as e:
            print(f"Error getting number of flights per aircraft: {e}")
        finally:
            self.close_connection()

    def total_number_of_pilots(self):
        try:
            self.get_connection()
            self.check_table_exists('Pilot')
            total_pilots_sql = "SELECT COUNT(*) FROM Pilot;"
            self.cur.execute(total_pilots_sql)
            total_pilots = self.cur.fetchone()[0]
            print("Total number of pilots:", total_pilots)
        except sqlite3.Error as e:
            print(f"Error getting total number of pilots: {e}")
        finally:
            self.close_connection()
