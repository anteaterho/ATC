import tkinter as tk
from tkinter import messagebox
import random as r

# Global variables for simulation
current_selection = 0
fields = []
probe_window_open = False
inventory_window_open = False
probe_items = []
log_data = ""
challenge_mode = False
mission = ""
mineral_data = {}

# Variables for the rocket launch simulation (user input for sandbox, random for challenge)
fuel_level = 0
weather_condition = ""
engine_temperature = 0
thrust_level = 0
oxygen_supply = ""
flight_path = ""
communication_status = ""
launch_readiness = False
attitude_control = ""
gravitational_influence = ""

# 로버 팔 상태
rover_arm_open = False

missions = [
    "Collect 5 samples from the designated planet.",
    "Reach a speed of at least 2000 km/h.",
    "Complete the mission within 60 seconds.",
    "Successfully separate the rocket stages.",
    "Return to Earth safely.",
    "Establish communication with the space station.",
    "Perform a spacewalk.",
    "Navigate through an asteroid belt.",
    "Conduct an experiment in zero gravity.",
    "Land on a moon of Jupiter.",
    "Rescue a stranded astronaut.",
    "Collect data from a comet.",
    "Repair the spacecraft's solar panels.",
    "Survey an alien planet for resources.",
    "Test the new propulsion system."
]

# 장애물 목록
obstacles = [
    "solar flare", "asteroid field", "black hole", "space debris", 
    "wormhole", "alien ship", "gravity well", "magnetic storm",
    "time vortex", "nebula", "supernova", "quantum anomaly", 
    "radiation zone", "void space", "spatial rift", "energy pulse",
    "plasma storm", "dark energy zone", "paradox field", 
    "spacetime rip", "heat death region", "dark matter surge", 
    "data corruption", "system overload", "power failure", 
    "communications blackout", "thermal shielding failure", 
    "engine malfunction", "crew panic", "alien interference", 
    "unexpected solar flare", "asteroid collision", "radiation leak", 
    "proximity alert", "reactor meltdown", "life support failure"
]

# 각 장애물에 대한 대처 방법
obstacle_solutions = {
    "solar flare": [
        "Activate solar shields.", "Change trajectory temporarily.", "Adjust power settings."
    ],
    "asteroid field": [
        "Engage evasive maneuvers.", "Increase speed to pass through.", "Utilize radar for navigation."
    ],
    "black hole": [
        "Reverse thrust to escape gravitational pull.", "Change course immediately.", "Prepare emergency systems."
    ],
    "space debris": [
        "Activate deflector shields.", "Perform manual navigation.", "Reduce speed and monitor surroundings."
    ],
    "wormhole": [
        "Prepare for sudden course change.", "Engage wormhole navigation system.", "Establish contact with mission control."
    ],
    # ... (중략) ...
    "life support failure": [
        "Check life support systems.", "Activate backup systems.", "Prepare for emergency evacuation."
    ]
}

# 로버 팔 열기 함수
def toggle_rover_arm():
    global rover_arm_open
    rover_arm_open = not rover_arm_open
    status = "opened" if rover_arm_open else "closed"
    messagebox.showinfo("Rover Arm Status", f"The rover arm has been {status}.")

# 광물 분석 함수
def analyze_mineral():
    if rover_arm_open:
        mineral_name = r.choice(["Iron", "Copper", "Silver", "Gold", "Platinum"])
        mineral_data[mineral_name] = r.randint(1, 100)  # Random quantity for analysis
        messagebox.showinfo("Mineral Analysis", f"Analyzed mineral: {mineral_name} - Quantity: {mineral_data[mineral_name]}")
    else:
        messagebox.showwarning("Rover Arm Closed", "Please open the rover arm first.")

# 장애물 처리 함수
def handle_obstacle(obstacle):
    solutions = obstacle_solutions.get(obstacle, ["No solution available"])
    message = f"You've encountered {obstacle}! How would you like to respond?\n"
    options = "\n".join([f"{i+1}. {solution}" for i, solution in enumerate(solutions)])
    messagebox.showinfo("Obstacle Encountered", message + options)

def encounter_obstacle():
    obstacle = r.choice(obstacles)
    handle_obstacle(obstacle)

# 로켓 발사 관련 변수 체크
def check_rocket_variables():
    issues = []
    
    if fuel_level < 80:
        issues.append(f"Low fuel level: {fuel_level}%")
    if weather_condition != "Clear":
        issues.append(f"Poor weather: {weather_condition}")
    if engine_temperature > 100:
        issues.append(f"Engine temperature too high: {engine_temperature}°C")
    if thrust_level < 80:
        issues.append(f"Insufficient thrust: {thrust_level}%")
    if oxygen_supply != "Normal":
        issues.append(f"Oxygen supply issue: {oxygen_supply}")
    if flight_path != "Stable":
        issues.append(f"Flight path deviation: {flight_path}")
    if communication_status != "Good":
        issues.append(f"Communication issue: {communication_status}")
    if not launch_readiness:
        issues.append("Launch readiness incomplete")
    if attitude_control != "Stable":
        issues.append(f"Attitude control problem: {attitude_control}")
    if gravitational_influence != "Nominal":
        issues.append(f"Gravitational influence too high: {gravitational_influence}")
    
    return issues

# 로그 저장
def save_log():
    global log_data
    try:
        with open("rocket_log.txt", "w") as file:
            file.write(log_data)
        messagebox.showinfo("Log Saved", "Rocket launch log saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save log: {str(e)}")

# 로그 불러오기
def load_log():
    global log_data
    try:
        with open("rocket_log.txt", "r") as file:
            log_data = file.read()
        messagebox.showinfo("Log Loaded", "Rocket launch log loaded successfully.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Log file not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load log: {str(e)}")

# 로켓 발사 시 시뮬레이션 실행 함수
def launch_simulation():
    global fuel_level, weather_condition, engine_temperature, thrust_level
    global oxygen_supply, flight_path, communication_status, launch_readiness
    global attitude_control, gravitational_influence
    
    # 챌린지 모드에서 변수를 임의로 설정
    if challenge_mode:
        fuel_level = r.randint(10, 20) * 5  # 연료량 (%)
        weather_condition = r.choice(["Clear", "Cloudy", "Stormy"])  # 기상 상태
        engine_temperature = r.randint(10, 20) * 5  # 엔진 온도 (섭씨)
        thrust_level = r.randint(10, 20) * 5  # 추진력 (%)
        oxygen_supply = r.choice(["Normal", "Low", "Critical"])  # 산소 공급 상태
        flight_path = r.choice(["Stable", "Deviated", "Critical"])  # 비행 경로
        communication_status = r.choice(["Good", "Intermittent", "Lost"])  # 통신 상태
        launch_readiness = r.choice([True, False])  # 발사 준비 완료 여부
        attitude_control = r.choice(["Stable", "Unstable", "Critical"])  # 자세 제어 상태
        gravitational_influence = r.choice(["Nominal", "High", "Extreme"])  # 중력 영향
    else:
        # 샌드박스 모드에서 사용자가 입력한 값을 가져옴
        fuel_level = int(entry_fuel_level.get())
        weather_condition = entry_weather_condition.get()
        engine_temperature = int(entry_engine_temperature.get())
        thrust_level = int(entry_thrust_level.get())
        oxygen_supply = entry_oxygen_supply.get()
        flight_path = entry_flight_path.get()
        communication_status = entry_communication_status.get()
        launch_readiness = bool(entry_launch_readiness.get())
        attitude_control = entry_attitude_control.get()
        gravitational_influence = entry_gravitational_influence.get()

    # 변수 검증 후 결과 출력
    issues = check_rocket_variables()

    if issues:
        issue_message = "\n".join(issues)
        messagebox.showwarning("Launch Issues", f"Rocket launch has issues:\n{issue_message}")
    else:
        messagebox.showinfo("Launch Success", "Rocket launch successful!")

    # 로그 저장
    log_rocket_launch()

# 로켓 발사 로그 기록
def log_rocket_launch():
    global log_data
    log_data += f"Fuel Level: {fuel_level}%\n"
    log_data += f"Weather Condition: {weather_condition}\n"
    log_data += f"Engine Temperature: {engine_temperature}°C\n"
    log_data += f"Thrust Level: {thrust_level}%\n"
    log_data += f"Oxygen Supply: {oxygen_supply}\n"
    log_data += f"Flight Path: {flight_path}\n"
    log_data += f"Communication Status: {communication_status}\n"
    log_data += f"Launch Readiness: {launch_readiness}\n"
    log_data += f"Attitude Control: {attitude_control}\n"
    log_data += f"Gravitational Influence: {gravitational_influence}\n\n"

# GUI 세팅
root = tk.Tk()
root.title("Rocket Simulation")

# Fuel Level Input
tk.Label(root, text="Fuel Level (%):").pack()
entry_fuel_level = tk.Entry(root)
entry_fuel_level.pack()

# Weather Condition Input
tk.Label(root, text="Weather Condition:").pack()
entry_weather_condition = tk.Entry(root)
entry_weather_condition.pack()

# Engine Temperature Input
tk.Label(root, text="Engine Temperature (°C):").pack()
entry_engine_temperature = tk.Entry(root)
entry_engine_temperature.pack()

# Thrust Level Input
tk.Label(root, text="Thrust Level (%):").pack()
entry_thrust_level = tk.Entry(root)
entry_thrust_level.pack()

# Oxygen Supply Input
tk.Label(root, text="Oxygen Supply:").pack()
entry_oxygen_supply = tk.Entry(root)
entry_oxygen_supply.pack()

# Flight Path Input
tk.Label(root, text="Flight Path:").pack()
entry_flight_path = tk.Entry(root)
entry_flight_path.pack()

# Communication Status Input
tk.Label(root, text="Communication Status:").pack()
entry_communication_status = tk.Entry(root)
entry_communication_status.pack()

# Launch Readiness Input
tk.Label(root, text="Launch Readiness (True/False):").pack()
entry_launch_readiness = tk.Entry(root)
entry_launch_readiness.pack()

# Attitude Control Input
tk.Label(root, text="Attitude Control:").pack()
entry_attitude_control = tk.Entry(root)
entry_attitude_control.pack()

# Gravitational Influence Input
tk.Label(root, text="Gravitational Influence:").pack()
entry_gravitational_influence = tk.Entry(root)
entry_gravitational_influence.pack()

# 버튼 생성
tk.Button(root, text="Launch Simulation", command=launch_simulation).pack()
tk.Button(root, text="Save Log", command=save_log).pack()
tk.Button(root, text="Load Log", command=load_log).pack()
tk.Button(root, text="Toggle Rover Arm", command=toggle_rover_arm).pack()
tk.Button(root, text="Analyze Mineral", command=analyze_mineral).pack()
tk.Button(root, text="Encounter Obstacle", command=encounter_obstacle).pack()

# 챌린지 모드 토글 버튼
def toggle_challenge_mode():
    global challenge_mode
    challenge_mode = not challenge_mode
    status = "enabled" if challenge_mode else "disabled"
    messagebox.showinfo("Challenge Mode", f"Challenge mode has been {status}.")

tk.Button(root, text="Toggle Challenge Mode", command=toggle_challenge_mode).pack()

root.mainloop()
