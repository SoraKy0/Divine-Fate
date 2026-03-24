import random
import customtkinter as ctk
import time
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ------------------ TIMER LOAD ------------------

def load_timer():
    try:
        with open("timer.txt", "r") as f:
            return float(f.read())
    except:
        return None

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

        if os.path.exists("timer.txt"):
            os.remove("timer.txt")

# ------------------ BUTTON ACTION ------------------

def roll_fate():
    global end_time

    choices = ["Draw", "Read Book", "Just Chill", "Learn Japanese", "Play Steam Deck"]

    colors = {
        "Draw": "#ff9f1c",
        "Read Book": "#4da6ff",
        "Just Chill": "#8c00ff",
        "Learn Japanese": "#00ffcc",
        "Play Steam Deck": "#ff4d4d"
    }

    choice = random.choice(choices)

    result.configure(
        text=f"Your Fate: {choice}",
        text_color=colors[choice]
    )

    button.configure(state="disabled")
    lock_label.pack()  # show lock

    end_time = time.time() + 600

    with open("timer.txt", "w") as f:
        f.write(str(end_time))

    update_timer()

# ------------------ UI ------------------

root = ctk.CTk()
root.title("Divine Fate")
root.geometry("350x300")

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

end_time = load_timer()

if end_time and end_time > time.time():
    button.configure(state="disabled")
    lock_label.pack()
    update_timer()

root.mainloop()