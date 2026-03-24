import random
import customtkinter as ctk
import time
import os
import sys
import json

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

STATE_FILE = "timer.txt"
CHOICES = ["Draw", "Read Book", "Just Chill", "Learn Japanese", "Play Steam Deck"]
COLORS = {
    "Draw": "#ff9f1c",
    "Read Book": "#4da6ff",
    "Just Chill": "#8c00ff",
    "Learn Japanese": "#00ffcc",
    "Play Steam Deck": "#ff4d4d"
}


def resource_path(filename):
    base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, filename)

# ------------------ STATE LOAD ------------------

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            saved = f.read().strip()

        if not saved:
            return {"end_time": None, "choice": None}

        try:
            state = json.loads(saved)
            return {
                "end_time": state.get("end_time"),
                "choice": state.get("choice")
            }
        except json.JSONDecodeError:
            return {"end_time": float(saved), "choice": None}
    except Exception:
        return {"end_time": None, "choice": None}


def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump({"end_time": end_time, "choice": current_choice}, f)


def clear_state():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

# ------------------ TIMER UPDATE ------------------

def update_timer():
    global end_time

    if end_time is None:
        return

    remaining = int(end_time - time.time())

    if remaining > 0:
        mins = remaining // 60
        secs = remaining % 60

        timer_label.configure(text=f"{mins}:{secs:02d}")
        root.after(1000, update_timer)
    else:
        timer_label.configure(text="Done!")
        button.configure(state="normal")
        lock_label.pack_forget()
        clear_state()

# ------------------ BUTTON ACTION ------------------

def roll_fate():
    global end_time, current_choice

    current_choice = random.choice(CHOICES)

    result.configure(
        text=f"Your Fate: {current_choice}",
        text_color=COLORS[current_choice]
    )

    button.configure(state="disabled")
    lock_label.pack()  # show lock

    end_time = time.time() + 600

    save_state()
    update_timer()

# ------------------ UI ------------------

root = ctk.CTk()
root.title("Divine Fate")
root.geometry("350x300")

try:
    root.iconbitmap(resource_path("divinetree.ico"))
except Exception:
    pass

title = ctk.CTkLabel(
    root,
    text="Choose Your Fate",
    font=("Segoe UI", 20, "bold")
)
title.pack(pady=20)

button = ctk.CTkButton(
    root,
    text="FATE",
    command=roll_fate,
    corner_radius=20,
    height=50,
    width=150,
    font=("Segoe UI", 14, "bold"),
    fg_color="#370057",
    hover_color="#5a0080"
)
button.pack(pady=15)

# Hover effect
def on_enter(e):
    button.configure(fg_color="#9d4edd")

def on_leave(e):
    button.configure(fg_color="#370057")

button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)

# Timer label
timer_label = ctk.CTkLabel(
    root,
    text="",
    font=("Segoe UI", 14),
    text_color="#ff4d4d"
)
timer_label.pack()

# Lock icon
lock_label = ctk.CTkLabel(
    root,
    text="❌ Locked",
    text_color="red",
    font=("Segoe UI", 14)
)

# Result
result = ctk.CTkLabel(
    root,
    text="",
    font=("Segoe UI", 14),
    text_color="green"
)
result.pack(pady=20)

# ------------------ RESUME TIMER ------------------

saved_state = load_state()
end_time = saved_state["end_time"]
current_choice = saved_state["choice"]

if current_choice in COLORS:
    result.configure(
        text=f"Your Fate: {current_choice}",
        text_color=COLORS[current_choice]
    )

if end_time and end_time > time.time():
    button.configure(state="disabled")
    lock_label.pack()
    update_timer()
else:
    end_time = None
    if current_choice is not None:
        clear_state()

root.mainloop()
