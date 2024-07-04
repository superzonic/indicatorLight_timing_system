import tkinter as tk
import serial.tools.list_ports
import serial
import threading
from datetime import datetime
import sqlite3
import counting

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Andon system")
        self.cancel_ids = [None] * 8  # Store ids for cancelling update

        # User interface
        self.create_menu_bar()
        self.create_top_image_row()
        self.create_bottom_labels()
        self.create_button_row()
    def create_bottom_labels(self):
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side="bottom", padx=5, pady=2, fill="x")
        self.downtime_labels = []  # Store labels to update later
        for i in range(8):
            label_text = self.get_total_downtime(i + 1)  # Get total downtime for line i+1
            # Truncate the seconds string to ensure only two digits are displayed
            seconds_index = label_text.rfind(':') + 1
            truncated_label_text = label_text[:seconds_index + 3]  # Include two digits for seconds and the colon
            label = tk.Label(bottom_frame, text=f"Line {i + 1} Total Downtime: {truncated_label_text}",
                             font=("Arial", 16), padx=10, pady=5)
            label.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.downtime_labels.append(label)  # Store label for later update
    def get_total_downtime(self, line_number, ):
        # Create an instance of the count_time class
        counter = counting.count_time(table_name=f"line{line_number}")
        return counter.get_total_time_for_current_date()

    def update_downtime_label(self, line_number):
        label_text = self.get_total_downtime(line_number)
        # Truncate the seconds string to ensure only two digits are displayed
        seconds_index = label_text.rfind(':') + 1
        truncated_label_text = label_text[:seconds_index + 3]  # Include two digits for seconds and the colon
        self.downtime_labels[(line_number - 1)].config(
            text=f"Line {line_number} Total Downtime: {truncated_label_text}")

    def create_menu_bar(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        setup_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Setup", menu=setup_menu)
        setup_menu.add_command(label="Settings")
    def create_top_image_row(self):
        top_image_frame = tk.Frame(self.root)
        top_image_frame.pack(padx=5, pady=2, fill="x")

        label = tk.Label(top_image_frame, text="Line Status",
                         font=("Arial", 35, "bold"), fg="#48adcf")
        label.pack(padx=1, pady=10)

    def create_button_row(self):
        # Create a frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=5, pady=2, fill="x")

        # Create and place the label for the highlighted topic text
        topic_label = tk.Label(self.root, text="Total down time today", font=("Helvetica", 16, "bold"))
        topic_label.pack(pady=20,padx=10)

        # Create buttons
        self.buttons = []
        self.button_states = [False] * 8  # Initial state of buttons (False for not clicked)
        for i in range(8):
            # Create button with lambda function to pass index
            button = tk.Button(button_frame, width=14, height=4, font=("Helvetica", 29),
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
            # Button is in True state
            line_count = counting.count_time(table_name="Line" + str(index + 1))  # Ensure the table name matches
            self.buttons[index].config(text=f"LINE {index + 1}\n\nNEED\n ATTENTION\n", bg="red",
                                       disabledforeground="black")
            if index in (0, 1):
                self.cancel_task(index)
                self.counting_text_edit(index, line_count)  # Call counting_text_edit directly
            else:
                self.cancel_ids[index] = self.buttons[index].after(1000, lambda idx=index, lc=line_count: self.counting_text_edit(idx, lc))
        else:
            # Button is in False state

            self.cancel_task(index)
            line_count = counting.count_time(table_name="Line" + str(index + 1))  # Ensure the table name matches
            total_downtime = self.get_total_downtime(index + 1)

            self.buttons[index].config(text=f"LINE {index + 1}\nRUNNING\n WELL\n {total_downtime}", bg="green",
                                       disabledforeground="black")
            def downtime_update():
                self.cancel_task(index)
                line_count = counting.count_time(table_name="Line" + str(index + 1))  # Ensure the table name matches
                total_downtime = self.get_total_downtime(index + 1)
                self.buttons[index].config(text=f"LINE {index + 1}\nRUNNING\n WELL\n {total_downtime}", bg="green",
                                           disabledforeground="black")


            self.buttons[index].after(5,downtime_update)
        # Update the button state
        self.button_states[index] = state
        self.update_downtime_label(index + 1)



    def cancel_task(self, index):
        if self.cancel_ids[index] is not None:
            self.root.after_cancel(self.cancel_ids[index])
            self.cancel_ids[index] = None
    def counting_text_edit(self, index, line_count):
        line_count.count_up()
        self.time_value = line_count.convert_seconds()
        total_downtime = self.get_total_downtime(index + 1)
        self.buttons[index].config(text=f"LINE {index + 1}\nNEED\n ATTENTION\n{self.time_value}\n {total_downtime}",
                                   bg="red", disabledforeground="black")
        self.cancel_ids[index] = self.buttons[index].after(1000, lambda idx=index, lc=line_count: self.counting_text_edit(idx, lc))
class Connector:
    def __init__(self, main_app):
        self.start_times = [None] * 8
        self.main_app = main_app

    def screen(self, signal):
        try:
            pin, state = signal.split()
            pin_number = int(pin[1])
            if state == "on" and self.start_times[pin_number] is None:
                self.start_times[pin_number] = datetime.now()
                print(f"Time started for X{pin_number}: {self.start_times[pin_number]}")
                self.main_app.update_button_text_color(pin_number, True)
                write_start_time_to_database(pin_number, self.start_times[pin_number])
            elif state == "off" and self.start_times[pin_number] is not None:
                end_time = datetime.now()
                print(f"Time stopped for X{pin_number}: {end_time}")
                self.main_app.update_button_text_color(pin_number, False)
                write_stop_time_to_database(pin_number, self.start_times[pin_number], end_time, self.main_app)
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
        conn = sqlite3.connect('line_data.db')
        c = conn.cursor()
        c.execute(f"INSERT INTO line{pin_number + 1} (Date, Start_time) VALUES (?, ?)",
                  (start_time.date(), start_time.time().strftime('%H:%M:%S')))
        conn.commit()
        conn.close()
        print("Start time written to database successfully")
    except Exception as e:
        print(f"Error writing start time to database: {e}")

def write_stop_time_to_database(pin_number, start_time, end_time, main_app_instance):
    try:
        conn = sqlite3.connect('line_data.db')
        c = conn.cursor()
        c.execute(f"UPDATE line{pin_number + 1} SET Stop_time = ? WHERE Start_time = ?",
                  (end_time.time().strftime('%H:%M:%S'), start_time.time().strftime('%H:%M:%S')))
        conn.commit()
        conn.close()
        print("Stop time written to database successfully")
        main_app_instance.update_downtime_label(pin_number + 1)
    except Exception as e:
        print(f"Error writing stop time to database: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1350x710")
    root.iconbitmap("icon.ico")
    app = MainApp(root)

    with open('port.txt', 'r') as file:
        port = file.read().strip()
    serialInst = serial.Serial()
    serialInst.baudrate = 9600
    serialInst.port = port
    serialInst.open()

    connector = Connector(app)
    threading.Thread(target=arduino_read, args=(serialInst, connector), daemon=True).start()

    root.mainloop()