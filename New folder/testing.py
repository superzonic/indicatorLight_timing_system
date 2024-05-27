import sqlite3
from datetime import datetime

def get_total_time_for_current_date(database_file, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Fetch entries for the current date
    cursor.execute(f"SELECT Start_time, Stop_time FROM {table_name} WHERE Date = ?", (current_date,))
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

if __name__ == "__main__":
    # Example usage
    database_file = "line_data.db"
    table_name = "line1"
    total_hours, total_minutes, total_seconds = get_total_time_for_current_date(database_file, table_name)
    print("Total time for today:", total_hours, "hours,", total_minutes, "minutes and", total_seconds, "seconds")
