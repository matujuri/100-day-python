from tkinter import Tk, Label, Button, Canvas, PhotoImage

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
TIME_LOGIC = [WORK_MIN, SHORT_BREAK_MIN, WORK_MIN, SHORT_BREAK_MIN, WORK_MIN, SHORT_BREAK_MIN, WORK_MIN, LONG_BREAK_MIN]
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps, timer
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    label.config(text="Timer", fg=GREEN)
    check_label.config(text="")
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    if reps == 0:
        check_label.config(text="")

    if TIME_LOGIC[reps] == LONG_BREAK_MIN:
        label.config(text="Break", fg=RED)
    elif TIME_LOGIC[reps] == SHORT_BREAK_MIN:
        label.config(text="Break", fg=PINK)
    else:
        label.config(text="Work", fg=GREEN)
    count_down(TIME_LOGIC[reps] * 60)
    # before count down start, reps is incremented
    reps += 1

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global reps, timer
    canvas.itemconfig(timer_text, text=f"{count // 60:02d}:{count % 60:02d}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        if reps % 2 == 1: # 完了したセッションのreps値が奇数インデックス (1, 3, 5, 7) に対応
            # 最前面に表示
            window.attributes('-topmost', True)
            window.focus_force()
            check_label.config(text="✔︎" * ((reps + 1) // 2))
            
        if reps < 8:
            start_timer()
        else:
            reps = 0
            label.config(text="Timer", fg=GREEN)
            

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)
# フォーカスを失ったら最前面解除
window.bind("<FocusOut>", lambda event: window.attributes('-topmost', False))

label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, "bold"))
label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
canvas.grid(column=1, row=1)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

start_button = Button(text="Start", highlightbackground=YELLOW, highlightthickness=0, command=start_timer).grid(column=0, row=2)
reset_button = Button(text="Reset", highlightbackground=YELLOW, highlightthickness=0, command=reset_timer).grid(column=2, row=2)
check_label = Label(fg=GREEN, bg=YELLOW)
check_label.grid(column=1, row=3)

window.mainloop()