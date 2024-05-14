import tkinter as tk
import serial.tools.list_ports
import serial
import threading
from datetime import datetime
import sqlite3

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Andon system")

        # User interface
        self.create_menu_bar()
        self.create_top_image_row()
        self.create_button_row()

    def create_menu_bar(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        setup_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Setup", menu=setup_menu)
        setup_menu.add_command(label="Settings")

    def create_top_image_row(self):
        top_image_frame = tk.Frame(self.root)
        top_image_frame.pack(padx=5, pady=2, fill="x")

        label = tk.Label(top_image_frame, text="Andon system",
                         font=("Arial", 40, "bold"), fg="#48adcf")
        label.pack(padx=1, pady=15)

    def create_button_row(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=5, pady=2, fill="x")
        self.buttons = []
        self.button_states = [False] * 8  # Initial state of buttons (False for not clicked)
        for i in range(8):
            button = tk.Button(button_frame, width=13, height=5, font=("Helvetica", 29),
                               command=lambda idx=i: self.toggle_button(idx))
            button.grid(row=0 if i < 4 else 1, column=i % 4, padx=1, pady=1)
            button.config(state="disabled")
            self.buttons.append(button)
            self.update_button_text_color(i)

    def toggle_button(self, index):
        self.button_states[index] = not self.button_states[index]
        self.update_button_text_color(index)

    def update_button_text_color(self, index, state=None):
        if state is None:
            state = self.button_states[index]
        if state:
            self.buttons[index].config(text=f"LINE {index + 1}\n\nNEED\n ATTENTION", bg="red" , disabledforeground= "black")
        else:
            self.buttons[index].config(text=f"LINE {index + 1}\n\nRUNNING\n WELL", bg="green" , disabledforeground="black")

class Connector:
    def __init__(self):
        self.start_times = [None] * 8

    def screen(self, signal):
        try:
            pin, state = signal.split()
            pin_number = int(pin[1])
            if state == "on" and self.start_times[pin_number] is None:
                self.start_times[pin_number] = datetime.now()
                print(f"Time started for X{pin_number}: {self.start_times[pin_number]}")
                app.update_button_text_color(pin_number, True)
                write_start_time_to_database(pin_number, self.start_times[pin_number])
            elif state == "off" and self.start_times[pin_number] is not None:
                end_time = datetime.now()
                print(f"Time stopped for X{pin_number}: {end_time}")
                app.update_button_text_color(pin_number, False)
                write_stop_time_to_database(pin_number, self.start_times[pin_number], end_time)
                self.start_times[pin_number] = None
        except Exception as e:
            print(f"Error processing signal: {e}")

def arduino_read(serialInst, connector):
    while True:
        if serialInst.in_waiting:
            try:
                signal = serialInst.readline().decode('utf-8').strip()
                connector.screen(signal)
            except UnicodeDecodeError as e:
                pass

def write_start_time_to_database(pin_number, start_time):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('line_data.db')
        c = conn.cursor()

        # Insert start time into the line table
        c.execute(f"INSERT INTO line{pin_number + 1} (Date, Start_time) VALUES (?, ?)",
                  (start_time.date(), start_time.time().strftime('%H:%M:%S')))

        # Commit changes and close connection
        conn.commit()
        conn.close()
        print("Start time written to database successfully")
    except Exception as e:
        print(f"Error writing start time to database: {e}")

def write_stop_time_to_database(pin_number, start_time, end_time):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('line_data.db')
        c = conn.cursor()

        # Update stop time in the line table
        c.execute(f"UPDATE line{pin_number + 1} SET Stop_time = ? WHERE Start_time = ?",
                  (end_time.time().strftime('%H:%M:%S'), start_time.time().strftime('%H:%M:%S')))

        # Commit changes and close connection
        conn.commit()
        conn.close()
        print("Stop time written to database successfully")
    except Exception as e:
        print(f"Error writing stop time to database: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1250x610")
    root.iconbitmap("icon.ico")
    app = MainApp(root)


    # Initialize serial communication
    with open('port.txt', 'r') as file:
        port = file.read().strip()
    serialInst = serial.Serial()
    serialInst.baudrate = 9600
    serialInst.port = port
    serialInst.open()

    # Create Connector instance
    connector = Connector()

    # Start a separate thread for reading serial data
    threading.Thread(target=arduino_read, args=(serialInst, connector), daemon=True).start()

    root.mainloop()
