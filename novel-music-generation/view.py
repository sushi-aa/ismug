import tkinter
from tkinter import Tk, Frame, TOP, LEFT, BOTTOM, RAISED, BOTH, RIGHT, Button

root = Tk()
frame = Frame(root)
grid = Frame(frame)
grid.grid(sticky="news", column=0, row=3, columnspan=1)

def configure_window(root, frame):
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry('800x600')
    root.title("User Feedback")
    root.resizable(width=True, height=True)
    root.protocol("WM_DELETE_WINDOW", quit)
    frame.grid(row=0, column=0, sticky='news')

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(2, weight=1)



def add_buttons(root, frame):
    like_button = Button(text='Like')
    neutral_button = Button(text='Meh')
    dislike_button = Button(text='Dislike')


    like_button.grid(row=0, column=0, sticky='news')
    neutral_button.grid(row=1, column=0, sticky='news')
    dislike_button.grid(row=2, column=0, sticky='news')



def startup():
    global root
    global frame

    configure_window(root, frame)

    add_buttons(root, frame)

    return root


def init():
    root = Tk()
    frame = Frame(root)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    frame.grid(row=0, column=0, sticky="news")
    grid = Frame(frame)
    grid.grid(sticky="news", column=0, row=0, columnspan=2)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    # example values
    btn = Button(frame, text='Like')
    btn.grid(column=0, row=0, sticky="news")
    btn1 = Button(frame, text='Neutral')
    btn1.grid(column=0, row=1, sticky='news')
    btn2 = Button(frame, text='Dislike')
    btn2.grid(column=0, row=2, sticky='news')

    frame.columnconfigure(tuple(range(5)), weight=1)
    frame.rowconfigure(tuple(range(5)), weight=1)

    root.mainloop()
    #root = startup()
    #root.mainloop()


if __name__ == '__main__':
    init()
