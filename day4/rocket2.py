import tkinter as tk
from tkinter import messagebox, filedialog
import random as r
import json

# Global variables for the simulation
CR, CT, Tm_, Stage = 0, 0, 0, 0
FT, EN, TL, d, VRs, v, vu = '', '', '', '', 0, 0, 0
resources = []  # 자원 포인트 리스트 초기화
samples_collected = []  # 수집한 샘플 리스트
robot_arm_extended = False  # 로봇 팔이 확장되었는지 여부
probe_position = [250, 250]  # 탐사선 위치 (리스트로 수정)

# Function to start the rocket launch
def launch_simulation():
    global CR, CT, Tm_, Stage, FT, EN, TL, d, VRs, v

    user_id = entry_user_id.get()
    user_dg = int(entry_user_dg.get())
    dg_titles = ['Stu.', 'Dr.', 'Prof.']

    if user_dg in [1, 2, 3]:
        welcome_label.config(text=f"Welcome, {dg_titles[user_dg-1]} {user_id}.")
    else:
        welcome_label.config(text="Invalid degree, try again.")
        return  # Degree invalid, exit the function

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
    CT = 100 // crs
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

# Inventory management functions
def open_inventory():
    inventory_window = tk.Toplevel(root)
    inventory_window.title("Inventory")

    # 인벤토리 리스트 박스
    inventory_listbox = tk.Listbox(inventory_window)
    inventory_listbox.pack(fill=tk.BOTH, expand=True)

    for sample in samples_collected:
        inventory_listbox.insert(tk.END, sample['name'])

    # 시료 분석 및 전송 기능
    def analyze_sample(event):
        selected_sample = inventory_listbox.curselection()
        if not selected_sample:
            messagebox.showerror("Error", "No sample selected.")
            return

        sample_info = samples_collected[selected_sample[0]]
        mineral = "Mineral: " + r.choice(["Silicate", "Carbonate", "Oxide"])
        location = "Location: " + sample_info['location']
        shape = "Shape: " + r.choice(["Circle", "Square"])
        
        analysis_result = f"{mineral}\n{location}\n{shape}"
        messagebox.showinfo("Analysis Result", analysis_result)

    inventory_listbox.bind("<Button-3>", analyze_sample)  # 우클릭으로 분석

    def transfer_sample(event):
        selected_sample = inventory_listbox.curselection()
        if not selected_sample:
            messagebox.showerror("Error", "No sample selected.")
            return

        sample_info = samples_collected[selected_sample[0]]
        messagebox.showinfo("Transfer", f"{sample_info['name']} has been transferred to the mothership.")

    inventory_listbox.bind("<Button-1>", lambda event: event.widget.select_set(inventory_listbox.curselection()))  # 왼쪽 클릭으로 선택
    inventory_listbox.bind("<Control-Button-1>", transfer_sample)  # Ctrl + 왼쪽 클릭으로 전송

# 탐사선 제어 기능
class ProbeControl:
    def __init__(self, master):
        self.master = master
        self.probe_window = tk.Toplevel(master)
        self.probe_window.title("Probe Control")

        self.up_button = tk.Button(self.probe_window, text="Up", command=lambda: move_probe("up"))
        self.up_button.pack()

        self.down_button = tk.Button(self.probe_window, text="Down", command=lambda: move_probe("down"))
        self.down_button.pack()

        self.left_button = tk.Button(self.probe_window, text="Left", command=lambda: move_probe("left"))
        self.left_button.pack()

        self.right_button = tk.Button(self.probe_window, text="Right", command=lambda: move_probe("right"))
        self.right_button.pack()

        self.collect_button = tk.Button(self.probe_window, text="Collect Sample (T)", command=collect_sample)
        self.collect_button.pack()

# 시료 수집 및 로봇팔 제어
def collect_sample():
    global robot_arm_extended
    robot_arm_extended = True
    sample_name = f"Sample {len(samples_collected) + 1}"
    sample_location = f"({probe_position[0]}, {probe_position[1]})"
    samples_collected.append({"name": sample_name, "location": sample_location})
    messagebox.showinfo("Sample Collection", f"{sample_name} collected at {sample_location}.")

# 탐사선 이동 기능
def move_probe(direction):
    if direction == "up":
        probe_position[1] -= 10
    elif direction == "down":
        probe_position[1] += 10
    elif direction == "left":
        probe_position[0] -= 10
    elif direction == "right":
        probe_position[0] += 10
    
    update_probe_position()

def update_probe_position():
    canvas.delete("probe")  # 현재 위치의 탐사선 제거
    canvas.create_rectangle(probe_position[0], probe_position[1], probe_position[0] + 30, probe_position[1] + 30, fill="gray", tags="probe")  # 탐사선 그리기

# Key input handling
def handle_keypress(event):
    if event.char == 't':
        collect_sample()
    elif event.char == 'e':
        open_inventory()  # 'e' 키로 인벤토리 열기
    elif event.char == 'p':
        ProbeControl(root)  # 'p' 키로 탐사선 제어 창 열기

# Save and load data functions
def save_data():
    data = {
        "user_id": entry_user_id.get(),
        "degree": entry_user_dg.get(),
        "rocket_id": entry_rocket_id.get(),
        "fuel_type": entry_fuel_type.get(),
        "engine_name": entry_engine_name.get(),
        "timer": entry_timer.get(),
        "charge_rate": entry_charge_rate.get(),
        "velocity_unit": entry_velocity_unit.get(),
        "speed_rate": entry_speed_rate.get(),
        "destination": entry_destination.get(),
        "distance": entry_distance.get(),
        "stage": entry_stage.get(),
        "samples_collected": samples_collected
    }

    with open("rocket_log.txt", "w") as file:
        json.dump(data, file, indent=4)
    messagebox.showinfo("Save", "Data saved successfully.")

def open_data():
    try:
        with open("rocket_log.txt", "r") as file:
            data = json.load(file)
            entry_user_id.delete(0, tk.END)
            entry_user_id.insert(0, data["user_id"])

            entry_user_dg.delete(0, tk.END)
            entry_user_dg.insert(0, data["degree"])

            entry_rocket_id.delete(0, tk.END)
            entry_rocket_id.insert(0, data["rocket_id"])

            entry_fuel_type.delete(0, tk.END)
            entry_fuel_type.insert(0, data["fuel_type"])

            entry_engine_name.delete(0, tk.END)
            entry_engine_name.insert(0, data["engine_name"])

            entry_timer.delete(0, tk.END)
            entry_timer.insert(0, data["timer"])

            entry_charge_rate.delete(0, tk.END)
            entry_charge_rate.insert(0, data["charge_rate"])

            entry_velocity_unit.delete(0, tk.END)
            entry_velocity_unit.insert(0, data["velocity_unit"])

            entry_speed_rate.delete(0, tk.END)
            entry_speed_rate.insert(0, data["speed_rate"])

            entry_destination.delete(0, tk.END)
            entry_destination.insert(0, data["destination"])

            entry_distance.delete(0, tk.END)
            entry_distance.insert(0, data["distance"])

            entry_stage.delete(0, tk.END)
            entry_stage.insert(0, data["stage"])

            global samples_collected
            samples_collected = data["samples_collected"]

            messagebox.showinfo("Load", "Data loaded successfully.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No saved data found.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Error reading the data file.")

# Main GUI setup
root = tk.Tk()
root.title("Rocket Launch Simulation")

# Input fields and labels setup
frame_inputs = tk.Frame(root)
frame_inputs.pack()

tk.Label(frame_inputs, text="User ID:").grid(row=0, column=0)
entry_user_id = tk.Entry(frame_inputs)
entry_user_id.grid(row=0, column=1)

tk.Label(frame_inputs, text="Degree:").grid(row=1, column=0)
entry_user_dg = tk.Entry(frame_inputs)
entry_user_dg.grid(row=1, column=1)

tk.Label(frame_inputs, text="Rocket ID:").grid(row=2, column=0)
entry_rocket_id = tk.Entry(frame_inputs)
entry_rocket_id.grid(row=2, column=1)

tk.Label(frame_inputs, text="Fuel Type:").grid(row=3, column=0)
entry_fuel_type = tk.Entry(frame_inputs)
entry_fuel_type.grid(row=3, column=1)

tk.Label(frame_inputs, text="Engine Name:").grid(row=4, column=0)
entry_engine_name = tk.Entry(frame_inputs)
entry_engine_name.grid(row=4, column=1)

tk.Label(frame_inputs, text="Timer:").grid(row=5, column=0)
entry_timer = tk.Entry(frame_inputs)
entry_timer.grid(row=5, column=1)

tk.Label(frame_inputs, text="Charge Rate:").grid(row=6, column=0)
entry_charge_rate = tk.Entry(frame_inputs)
entry_charge_rate.grid(row=6, column=1)

tk.Label(frame_inputs, text="Velocity Unit:").grid(row=7, column=0)
entry_velocity_unit = tk.Entry(frame_inputs)
entry_velocity_unit.grid(row=7, column=1)

tk.Label(frame_inputs, text="Speed Rate:").grid(row=8, column=0)
entry_speed_rate = tk.Entry(frame_inputs)
entry_speed_rate.grid(row=8, column=1)

tk.Label(frame_inputs, text="Destination:").grid(row=9, column=0)
entry_destination = tk.Entry(frame_inputs)
entry_destination.grid(row=9, column=1)

tk.Label(frame_inputs, text="Distance:").grid(row=10, column=0)
entry_distance = tk.Entry(frame_inputs)
entry_distance.grid(row=10, column=1)

tk.Label(frame_inputs, text="Stage:").grid(row=11, column=0)
entry_stage = tk.Entry(frame_inputs)
entry_stage.grid(row=11, column=1)

# Buttons and labels setup
launch_button = tk.Button(root, text="Launch Simulation", command=launch_simulation)
launch_button.pack()

save_button = tk.Button(root, text="Save Data", command=save_data)
save_button.pack()

load_button = tk.Button(root, text="Load Data", command=open_data)
load_button.pack()

# Text labels setup
welcome_label = tk.Label(root, text="")
welcome_label.pack()

charge_label = tk.Label(root, text="")
charge_label.pack()

percent_label = tk.Label(root, text="")
percent_label.pack()

countdown_label = tk.Label(root, text="")
countdown_label.pack()

flight_status_label = tk.Label(root, text="")
flight_status_label.pack()

# Canvas setup in a separate window
canvas_window = tk.Toplevel(root)
canvas_window.title("Canvas Window")
canvas = tk.Canvas(canvas_window, width=600, height=600, bg="black")
canvas.pack()

# Key event binding
root.bind("<Key>", handle_keypress)

# Initialize probe position
update_probe_position()

# Start main loop
root.mainloop()
