import math
from math import floor
from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECKMARK = "✔"
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    # stop timer
    # noinspection PyTypeChecker
    window.after_cancel(timer)
    # set timer_text to "00:00"
    canvas.itemconfig(timer_text, text="00:00")
    # set title_label to "Timer"
    title_label.config(text="Timer", fg=GREEN)
    # reset checks_label to an empty string
    checks_label.config(text="")

    global reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps

    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # if it's the 1st/3rd/5th/7th rep, use work_sec
    # if it's the 2nd/4th/6th rep, use short_break_sec
    # if it's the 8th rep, use long_break_sec
    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
# can't use timer.sleep() since the app is an event-driven application
def count_down(count):
    # time in format "mm:ss"
    minutes = floor(count / 60)
    seconds = count % 60

    # dynamic typing
    if seconds < 10:
        seconds = f"0{seconds}"

    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        # countdown completed - every two reps is a work session
        work_sessions = math.floor(reps / 2)
        if work_sessions > 0:
            checkmarks = ""
            for _ in range(work_sessions):
                checkmarks += CHECKMARK
            checks_label.config(text=checkmarks)

        # start the next timer
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

def say_something(a, b, c):
    print(a)
    print(b)
    print(c)

# waits an amount of time an invokes a function
# window.after(1000, say_something, 3, 5, 8)

# add image to window
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# image is centered
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)


# title
title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, "bold"))
title_label.grid(column=1, row=0)

# start button
start_button = Button(text="Start", highlightthickness=0, font=('Arial', 24), command=start_timer)
start_button.grid(column=0, row=2)

# reset button
reset_button = Button(text="Reset", highlightthickness=0, font=('Arial', 24), command=reset_timer)
reset_button.grid(column=2 ,row=2)

# checks label
checks_label = Label(fg=GREEN, bg=YELLOW, font=('Arial', 16))
checks_label.grid(column=1, row=3)




window.mainloop()