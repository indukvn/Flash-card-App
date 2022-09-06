from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
current_card = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfigure(lang, text="French", fill="black")
    canvas.itemconfigure(word, text=current_card["French"], fill="black")
    canvas.itemconfigure(front_img, image=front)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfigure(front_img, image=back)
    canvas.itemconfigure(lang, text="English", fill="white")
    canvas.itemconfigure(word, text=current_card["English"], fill="white")


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=40, pady=40, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526)
back = PhotoImage(file="images/card_back.png")
front = PhotoImage(file="images/card_front.png")
front_img = canvas.create_image(400, 263, image=front)


lang = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

no = PhotoImage(file="images/wrong.png")
btn1 = Button(image=no, highlightthickness=0, command=next_card)
btn1.grid(row=1, column=0)

yes = PhotoImage(file="images/right.png")
btn2 = Button(image=yes, highlightthickness=0, command=is_known)
btn2.grid(row=1, column=1)

next_card()

if btn2:
    to_learn


window.mainloop()