import tkinter as tk
from tkinter import messagebox
import time
import math as m
import random as r

# Global variables for the simulation
CR, CT, Tm_, Stage = 0, 0, 0, 0
FT, EN, ET, TL, d, VRs, At, v, vu = '', '', '', '', 0, 0, 0, 0, ''

# Function to start the rocket launch
def launch_simulation():
    global CR, CT, Tm_, Stage, FT, EN, ET, TL, d, VRs, At, v, vu

    user_id = entry_user_id.get()
    user_dg = int(entry_user_dg.get())
    dg_titles = ['Stu.', 'Dr.', 'Prof.']

    if user_dg in [1, 2, 3]:
        welcome_label.config(text=f"Welcome, {dg_titles[user_dg-1]} {user_id}.")
    else:
        welcome_label.config(text="Invalid degree, try again.")

    ft = entry_fuel_type.get()
    en = entry_engine_name.get()
    tl = entry_destination.get()

    try:
        timer = int(entry_timer.get())
        crs = int(entry_charge_rate.get())
        VRs = int(entry_speed_rate.get())
        distance = int(entry_distance.get())
        stage = int(entry_stage.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")
        return

    # Update variables for simulation
    CR = 0
    CT = m.ceil(100 / crs)
    Tm_ = timer
    Stage = stage
    FT, EN, TL, d, VRs, v = ft, en, tl, distance, VRs, 0
    vu = entry_velocity_unit.get()

    # Start charging fuel
    charge_fuel(crs)

def charge_fuel(crs):
    global CR, CT
    if CT >= 0 and CR <= 100:
        charge_label.config(text=f"{FT} fuel will be charged in T-{CT} seconds")
        percent_label.config(text=f"{CR}% charged")
        CT -= 1
        CR += crs
        root.after(1000, lambda: charge_fuel(crs))  # Loop with 1-second delay
    else:
        percent_label.config(text="100% charged")
        charge_label.config(text="<<<CHARGE COMPLETE>>>")
        time.sleep(1)
        launch_countdown()

def launch_countdown():
    global Tm_
    if Tm_ > 0:
        countdown_label.config(text=f"Rocket will be launched in T-{Tm_} seconds")
        Tm_ -= 1
        root.after(1000, launch_countdown)
    else:
        messagebox.showinfo("Launch", "Launch Sequence Ready!")
        launch_approval()

def launch_approval():
    def approve_launch():
        messagebox.showinfo("Launch", "Launch allowed.")
        simulate_flight()

    def deny_launch():
        messagebox.showinfo("Launch", "Launch denied.")
        root.quit()

    approve_button = tk.Button(root, text="Approve Launch", command=approve_launch)
    deny_button = tk.Button(root, text="Deny Launch", command=deny_launch)
    approve_button.pack()
    deny_button.pack()

def simulate_flight():
    global v, d, At, VRs
    if d > 0:
        v += VRs
        d -= v
        At = int(d / v)
        flight_status_label.config(text=f"Current speed: {v} {vu}. Destination in {At} seconds, {d} km left.")
        root.after(1000, simulate_flight)
    else:
        messagebox.showinfo("Destination", f"Welcome to {TL}")

def open_probe_window():
    probe_window = tk.Toplevel(root)
    probe_window.title("Probe Control")

    probe_name_label = tk.Label(probe_window, text="Probe Name")
    probe_name_label.pack()
    probe_name_entry = tk.Entry(probe_window)
    probe_name_entry.pack()

    probe_countdown_label = tk.Label(probe_window, text="Probe Separation Countdown")
    probe_countdown_label.pack()
    probe_countdown_entry = tk.Entry(probe_window)
    probe_countdown_entry.pack()

    def start_probe_separation():
        try:
            psc = int(probe_countdown_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid countdown.")
            return
        for i in range(psc, 0, -1):
            probe_status_label.config(text=f"{probe_name_entry.get()} probe is separated in T-{i} seconds")
            probe_window.update()
            time.sleep(1)
        messagebox.showinfo("Probe", f"{probe_name_entry.get()} probe separated successfully!")

    start_button = tk.Button(probe_window, text="Start Separation", command=start_probe_separation)
    start_button.pack()

    probe_status_label = tk.Label(probe_window, text="")
    probe_status_label.pack()

# Main tkinter window
root = tk.Tk()
root.title("Rocket Launch Simulation")
root.geometry("350x350")
# Labels and input fields
tk.Label(root, text="User ID:").pack()
entry_user_id = tk.Entry(root)
entry_user_id.pack()

tk.Label(root, text="Degree (1: Student, 2: Dr., 3: Prof.):").pack()
entry_user_dg = tk.Entry(root)
entry_user_dg.pack()

tk.Label(root, text="Fuel Type:").pack()
entry_fuel_type = tk.Entry(root)
entry_fuel_type.pack()

tk.Label(root, text="Engine Name:").pack()
entry_engine_name = tk.Entry(root)
entry_engine_name.pack()

tk.Label(root, text="Timer (seconds):").pack()
entry_timer = tk.Entry(root)
entry_timer.pack()

tk.Label(root, text="Charge Rate (per second):").pack()
entry_charge_rate = tk.Entry(root)
entry_charge_rate.pack()

tk.Label(root, text="Velocity Unit:").pack()
entry_velocity_unit = tk.Entry(root)
entry_velocity_unit.pack()

tk.Label(root, text="Target Speed:").pack()
entry_speed_rate = tk.Entry(root)
entry_speed_rate.pack()

tk.Label(root, text="Destination:").pack()
entry_destination = tk.Entry(root)
entry_destination.pack()

tk.Label(root, text="Distance (km):").pack()
entry_distance = tk.Entry(root)
entry_distance.pack()

tk.Label(root, text="Stage:").pack()
entry_stage = tk.Entry(root)
entry_stage.pack()

# Welcome label to show user details
welcome_label = tk.Label(root, text="")
welcome_label.pack()

# Buttons
start_button = tk.Button(root, text="Start Launch", command=launch_simulation)
start_button.pack()

probe_button = tk.Button(root, text="Control Probe", command=open_probe_window)
probe_button.pack()

# Status labels
charge_label = tk.Label(root, text="")
charge_label.pack()

percent_label = tk.Label(root, text="")
percent_label.pack()

countdown_label = tk.Label(root, text="")
countdown_label.pack()

flight_status_label = tk.Label(root, text="")
flight_status_label.pack()

# Start the tkinter main loop
root.mainloop()
