import tkinter as tk
from tkinter import Tk, Frame, TOP, LEFT, BOTTOM, RAISED, BOTH, RIGHT, Button
from functools import partial

def btnfunc(btnVal):
    print(f"{btnVal} pressed")

def init():
    root = Tk()
    frame = Frame(root)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.geometry('500x400')
    frame.grid(row=0, column=0, sticky="news")
    grid = Frame(frame)
    grid.grid(sticky="news", column=0, row=0, columnspan=1)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    prompt = tk.Label(text="How does this music match your state?", font=("Arial", 18))
    prompt.grid(column=0, row=0, sticky="new")
    prompt.grid()
    # example values
    btn = Button(frame, text='Very satisfied', font=("Arial", 12), command=partial(btnfunc, 4))
    btn.grid(column=0, row=1, sticky="news", padx=10, pady=2)
    btn1 = Button(frame, text='Satisfied', font=("Arial", 12), command=partial(btnfunc, 3))
    btn1.grid(column=0, row=2, sticky='news', padx=10, pady=1)
    btn1 = Button(frame, text='Neutral', font=("Arial", 12), command=partial(btnfunc, 2))
    btn1.grid(column=0, row=3, sticky='news', padx=10, pady=1)
    btn1 = Button(frame, text='Dissatisfied', font=("Arial", 12), command=partial(btnfunc, 1))
    btn1.grid(column=0, row=4, sticky='news', padx=10, pady=1)
    btn2 = Button(frame, text='Very dissatified', font=("Arial", 12), command=partial(btnfunc, 0))
    btn2.grid(column=0, row=5, sticky='news', padx=10, pady=2)

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(tuple(range(6)), weight=1)

    root.mainloop()
    #root = startup()
    #root.mainloop()


if __name__ == '__main__':
    init()

# Button callbacks, onclick functions [X]
# Connect these questions to HCI literature - could use Likert scale 
#   https://www.scribbr.com/methodology/likert-scale/
#   find literature tho
# Prompt/question: "How does this music match your state?"
# Options to play, pause, skip/regenerate, repeat?