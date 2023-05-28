import json
from tkinter import *
from tkinter import messagebox
from random import choice

FONT = ("aerial", 15)
PARAGRAPH_FONT= ("aerial", 12)
MIN = 1
# SEC = MIN * 60
SECOND = 60
#========= Functions ============
def choose_paragraph():
    with open("data.json") as data:
        all_paragraphs = json.load(data)
        p_index, paragraph = choice(list(all_paragraphs.items()))
    return paragraph


def check() -> tuple:
    original = paragraph.split(" ")
    typed = user_input.get("1.0", "end-1c").split(" ")
    print(f"typed: {typed}")
    print(f"original: {original}")
    cwpm = error = 0
    wpm = len(typed)
    for index in range(len(typed)):
        if typed[index] == original[index]:
            cwpm += 1
        else:
            error += 1
    return wpm, cwpm, error

def reset():
    global paragraph, SEC
    SEC = 60
    paragraph = choose_paragraph()
    paragraph_text.config(state = "normal")
    paragraph_text.delete("1.0", "end")
    paragraph_text.insert("1.0", paragraph)
    paragraph_text.config(state = "disabled")

    user_input.config(state="normal")
    user_input.delete("1.0", "end")

def write_highscore(cwpm):
    with open("highscore.txt", "r") as file:
        highscore = int(file.read())
    if (cwpm > highscore):
        with open("highscore.txt", 'w') as file:
            file.write(str(cwpm))


def count_down(SEC):
    if (SEC <=0):
        user_input.config(state="disabled")
        wpm, cwpm, error = check()
        write_highscore(cwpm=cwpm)
        is_continue = messagebox.askokcancel(title="continue? ", message=f"word per minute: {wpm} wpm\n"
                                                        f"corrected word per minute: {cwpm} cwpm\n"
                                                        f" made: {error} errors.\n"
                                                        f"do you wanted to continue?")
        if is_continue:
            reset()
            count_down(SEC= SECOND)
    else:
        window.after(1000, count_down, SEC-1)


window = Tk()
window.minsize(width=1000, height=500)
window.config(padx=30, pady=20)

paragraph = choose_paragraph()

paragraph_text = Text(height=10, width=110, font=PARAGRAPH_FONT, wrap="word", spacing2=6, pady=4, padx=10)
paragraph_text.insert(END, paragraph)
paragraph_text.grid(row=2, column=1, columnspan=5)
paragraph_text.config(state="disabled")

user_input = Text(height=7, width=110, font=PARAGRAPH_FONT, wrap="word", spacing2=6, pady=5, padx=10)
user_input.grid(row =3, column = 1, columnspan=5)
user_input.focus()
count_down(SECOND)

window.mainloop()
