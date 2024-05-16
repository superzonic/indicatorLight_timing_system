import sqlite3
from datetime import datetime

class count_time:
    def __init__(self,seconds = 0 , total_time = 0,database_file = "line_data.db" ,table_name=""):
        self.seconds = seconds
        self.total_time = total_time
        self.database_file = database_file
        self.table_name = table_name
    def convert_seconds(self):
        # Calculate hours, minutes, and remaining seconds
        hours = (self.seconds) // 3600
        minutes = (self.seconds % 3600) // 60
        seconds = self.seconds % 60

        return hours, minutes, seconds

    def count_up(self):
        self.seconds +=1

    def get_total_time_for_current_date(self):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()

        # Get the current date
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Fetch entries for the current date
        cursor.execute(f"SELECT Start_time, Stop_time FROM {self.table_name} WHERE Date = ?", (current_date,))
        entries = cursor.fetchall()

        total_time = 0
        # Calculate total time
        for start_time, stop_time in entries:
            start = datetime.strptime(start_time, '%H:%M:%S')
            stop = datetime.strptime(stop_time, '%H:%M:%S')
            duration = stop - start
            total_time += duration.seconds

        # Convert total seconds to hours, minutes, and seconds
        total_hours = total_time // 3600
        total_minutes = (total_time % 3600) // 60
        total_seconds = total_time

        # Close the connection
        conn.close()

        return total_hours, total_minutes, total_seconds





