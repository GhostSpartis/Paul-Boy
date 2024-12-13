import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import threading
import time

def update_clock():
    """Update the clock display to show the current time."""
    current_time = datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)

def check_alarm():
    """Continuously check if the current time matches the alarm time."""
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        alarm_set_time = f"{hour_var.get():02}:{minute_var.get():02}:{second_var.get():02}"
        if alarm_set_time == current_time:
            messagebox.showinfo("Alarm", "It's time!")
            break
        time.sleep(1)

def set_alarm():
    """Start a thread to check the alarm time."""
    alarm_thread = threading.Thread(target=check_alarm, daemon=True)
    alarm_thread.start()

# Create the main tkinter window
root = tk.Tk()
root.title("Clock with Alarm")
root.geometry("300x300")

# Create and place the clock label
clock_label = tk.Label(root, text="", font=("Helvetica", 48))
clock_label.pack(pady=20)

# Create frames for dial input
frame = tk.Frame(root)
frame.pack(pady=10)

# Variables to hold alarm time
hour_var = tk.IntVar(value=0)
minute_var = tk.IntVar(value=0)
second_var = tk.IntVar(value=0)

# Hour dial
hour_label = tk.Label(frame, text="Hour", font=("Helvetica", 12))
hour_label.grid(row=0, column=0, padx=5)
hour_spinbox = ttk.Spinbox(frame, from_=0, to=23, textvariable=hour_var, width=5, font=("Helvetica", 12))
hour_spinbox.grid(row=1, column=0, padx=5)

# Minute dial
minute_label = tk.Label(frame, text="Minute", font=("Helvetica", 12))
minute_label.grid(row=0, column=1, padx=5)
minute_spinbox = ttk.Spinbox(frame, from_=0, to=59, textvariable=minute_var, width=5, font=("Helvetica", 12))
minute_spinbox.grid(row=1, column=1, padx=5)

# Second dial
second_label = tk.Label(frame, text="Second", font=("Helvetica", 12))
second_label.grid(row=0, column=2, padx=5)
second_spinbox = ttk.Spinbox(frame, from_=0, to=59, textvariable=second_var, width=5, font=("Helvetica", 12))
second_spinbox.grid(row=1, column=2, padx=5)

# Create and place the set alarm button
set_alarm_button = tk.Button(root, text="Set Alarm", command=set_alarm, font=("Helvetica", 14))
set_alarm_button.pack(pady=20)

# Start the clock update loop
update_clock()

# Run the tkinter main loop
root.mainloop()