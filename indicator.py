import tkinter as tk
import serial.tools.list_ports
import serial
import threading

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Indicator lighting system")

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

        label = tk.Label(top_image_frame, text="Indicator lighting system",
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
            self.buttons.append(button)
            self.update_button_text_color(i)

    def toggle_button(self, index):
        self.button_states[index] = not self.button_states[index]
        self.update_button_text_color(index)

    def update_button_text_color(self, index, state=None):
        if state is None:
            state = self.button_states[index]
        if state:
            self.buttons[index].config(text=f"LINE {index + 1}\n\nNEED\n ATTENTION", bg="red")
        else:
            self.buttons[index].config(text=f"LINE {index + 1}\n\nRUNNING\n WELL", bg="green")

class Connector:
    def __init__(self, signal1):
        self.signal1 = signal1

    def screen(self):
        if self.signal1 == "OKAY":
            print("time started")
            app.update_button_text_color(0, True)
        elif self.signal1 == "not okay":
            print("time stopped")
            app.update_button_text_color(0, False)
        else:
            print(self.signal1)

def arduino_read(serialInst):
    if serialInst.in_waiting:
        try:
            packet = serialInst.readline()
            return packet.decode('utf-8').rstrip()
        except UnicodeDecodeError as e:
            print(f"UnicodeDecodeError: {e}")
            # Handle the error (e.g., ignore or replace invalid characters)
            return ""

def check_signal(serialInst):
    while True:
        x = arduino_read(serialInst)
        if x:
            tes = Connector(x)
            tes.screen()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1250x610")
    app = MainApp(root)

    # Initialize serial communication
    ports = serial.tools.list_ports.comports()
    serialInst = serial.Serial()
    serialInst.baudrate = 9600
    serialInst.port = "COM6"
    serialInst.open()

    # Start a separate thread for checking the signal
    threading.Thread(target=check_signal, args=(serialInst,), daemon=True).start()

    root.mainloop()
