from tkinter import Tk, Canvas, Button, PhotoImage
import pandas as pd
import random

# ---------------------------- CONSTANTS ------------------------------- #

FONT = ("Arial", 40, "italic")
FONT_BOLD = ("Arial", 60, "bold")

BACKGROUND_COLOR = "#B1DDC6"
WHITE_COLOR = "#FFFFFF"
BLACK_COLOR = "#000000"

ORIGINAL_FILE_PATH = "data/french_words.csv"
NEW_FILE_PATH = "data/words_to_learn.csv"

# ---------------------------- DATA ------------------------------- #
try:
    data = pd.read_csv(NEW_FILE_PATH)
except FileNotFoundError:
    data = pd.read_csv(ORIGINAL_FILE_PATH)

to_learn = data.to_dict(orient="records")

current_card = {}


# ---------------------------- CARD FUNCTIONS ------------------------------- #

def flip_card():
    canvas.itemconfig(title_text, text="English")
    canvas.itemconfig(title_text, fill=WHITE_COLOR)
    canvas.itemconfig(word_text, text=current_card["English"])
    canvas.itemconfig(word_text, fill=WHITE_COLOR)
    canvas.itemconfig(card_image, image=card_back_img)

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer) # cancel the timer if it is running
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_text, text="French")
    canvas.itemconfig(title_text, fill=BLACK_COLOR)
    canvas.itemconfig(word_text, text=current_card["French"])
    canvas.itemconfig(word_text, fill=BLACK_COLOR)
    canvas.itemconfig(card_image, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)
    
# ---------------------------- BUTTON FUNCTIONS ------------------------------- #

def is_known():
    to_learn.remove(current_card)
    pd.DataFrame(to_learn).to_csv(NEW_FILE_PATH, index=False)
    next_card()

def is_unknown():
    next_card()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="", font=FONT, fill="black")
word_text = canvas.create_text(400, 263, text="", font=FONT_BOLD, fill="black")
canvas.grid(row=0, column=0, columnspan=2)

right_img = PhotoImage(file="images/right.png")
button_right = Button(image=right_img, highlightthickness=0, command=is_known)
button_right.grid(row=1, column=0)

wrong_img = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=wrong_img, highlightthickness=0, command=is_unknown)
button_wrong.grid(row=1, column=1)

next_card()


window.mainloop()