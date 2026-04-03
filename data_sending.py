import tkinter as tk
from obswebsocket import obsws, requests

# ---------------- OBS CONNECT ----------------
ws = obsws("localhost", 4455, "1Sd99kwaG76GWXVv")
ws.connect()

# ---------------- DATA ----------------
blue_score = 0
red_score = 0
timer = 0   # seconds
running = False

# ---------------- FUNCTIONS ----------------
def format_time(t):
    m = t // 60
    s = t % 60
    return f"{m}:{s:02}"   # 3:00 format

def safe_call(req):
    try:
        ws.call(req)
    except Exception as e:
        print("OBS Error:", e)

def update_obs():
    safe_call(requests.SetInputSettings(
        inputName="blue_score",
        inputSettings={"text": str(blue_score)},
        overlay=True
    ))

    safe_call(requests.SetInputSettings(
        inputName="red_score",
        inputSettings={"text": str(red_score)},
        overlay=True
    ))

    safe_call(requests.SetInputSettings(
        inputName="blue_team",
        inputSettings={"text": blue_name.get()},
        overlay=True
    ))

    safe_call(requests.SetInputSettings(
        inputName="red_team",
        inputSettings={"text": red_name.get()},
        overlay=True
    ))

    safe_call(requests.SetInputSettings(
        inputName="line_follower_timer",
        inputSettings={"text": format_time(timer)},
        overlay=True
    ))

# ---------------- SCORE ----------------
def add_blue():
    global blue_score
    blue_score += 5
    update_obs()

def add_red():
    global red_score
    red_score += 5
    update_obs()

# ---------------- TIMER ----------------
def update_timer():
    global timer, running

    if running and timer > 0:
        timer -= 1
        update_obs()
    elif timer == 0:
        running = False

    root.after(1000, update_timer)

def start_timer():
    global running, timer

    if timer == 0:
        try:
            minutes = int(timer_entry.get())
            timer = minutes * 60
        except:
            timer = 0

    running = True

def stop_timer():
    global running
    running = False

def reset_all():
    global timer, blue_score, red_score, running
    timer = 0
    blue_score = 0
    red_score = 0
    running = False
    update_obs()

# ---------------- UI ----------------
root = tk.Tk()
root.title("Scoreboard Controller")

# Team names
tk.Label(root, text="Blue Team").grid(row=0, column=0)
blue_name = tk.Entry(root)
blue_name.insert(0, "BLUE")
blue_name.grid(row=0, column=1)

tk.Label(root, text="Red Team").grid(row=1, column=0)
red_name = tk.Entry(root)
red_name.insert(0, "RED")
red_name.grid(row=1, column=1)

tk.Button(root, text="Update Names", command=update_obs)\
    .grid(row=2, column=0, columnspan=2)

# Score buttons
tk.Button(root, text="Blue +5", width=15, command=add_blue)\
    .grid(row=3, column=0)

tk.Button(root, text="Red +5", width=15, command=add_red)\
    .grid(row=3, column=1)

# Timer input
tk.Label(root, text="Timer (minutes)").grid(row=4, column=0)
timer_entry = tk.Entry(root)
timer_entry.insert(0, "3")
timer_entry.grid(row=4, column=1)

# Timer controls
tk.Button(root, text="Start", command=start_timer)\
    .grid(row=5, column=0)

tk.Button(root, text="Stop", command=stop_timer)\
    .grid(row=5, column=1)

tk.Button(root, text="Reset", command=reset_all)\
    .grid(row=6, column=0, columnspan=2)

# Start loop
update_timer()

# Initial push to OBS
update_obs()

root.mainloop()