#create the object from this
import sqlite3
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd
from PIL import ImageTk, Image

import input_output_tester

import input_output_tester
signal_counter = 0

import tkinter as tk

class mainApp:
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
        label.grid(row=0, column=0, columnspan=8, padx=1, pady=15)

    def create_button_row(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=5, pady=2, fill="x")
        self.buttons = []
        self.button_states = [False] * 8  # Initial state of buttons (False for not clicked)
        for i in range(8):
            button = tk.Button(button_frame, width=13, height=5,font = ("Helvetica", 29),
 command=lambda idx=i: self.toggle_button(idx))
            button.grid(row=0 if i < 4 else 1, column=i % 4, padx=1, pady=1)
            self.buttons.append(button)
            self.update_button_text_color(i)
            # Set font size for button text

    def toggle_button(self, index):
        self.button_states[index] = not self.button_states[index]
        self.update_button_text_color(index)

    def update_button_text_color(self, index):
        if self.button_states[index]:
            self.buttons[index].config(text=f"Button {index+1}\nClicked", bg="red",)
        else:
            self.buttons[index].config(text=f"Button {index+1}\nNot Clicked", bg="green",)

class connector:
    def __init__(self, signal1): #checking for one input
        self.signal1 = signal1

    def screen(self):
        if self.signal1 == "OKAY":
            print("time started")
        elif self.signal1 == "not okay":
            print("time stopped")
        else:
            print(self.signal1)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1250x610")
    app = mainApp(root)
    root.mainloop()
    while True:

        x = str(input_output_tester.arduino_read())
        if x != "":
            tes = connector((x))
            tes.screen()
            signal_counter += 1
            print(signal_counter)