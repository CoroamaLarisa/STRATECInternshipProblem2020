from tkinter import *

from Console.Console import Console
from GUI_Package.GUI_step_four import menu_GUI

console = Console()


def gui():
    root = Tk()

    text_beginning = Label(root, text="Stratec Internship Problem")

    text_beginning.pack()

    topFrame = Frame(root)
    topFrame.pack()
    bottomFrame = Frame(root)
    bottomFrame.pack(side=BOTTOM)
    photo = PhotoImage(file="Stratec.png")
    label_photo = Label(root, image=photo)
    label_photo.pack(side=TOP)
    step_one_button = Button(topFrame, text="Step One", fg='red', command=lambda: console.Step_One("Step_One.csv",
                                                                                                   "Step_One_Solved.csv"))
    step_one_button.pack(side=LEFT)
    step_two_button = Button(topFrame, text="Step Two", fg='blue', command=lambda: console.Step_Two("Step_Two.csv",
                                                                                                    "Step_Two_Solved.csv"))
    step_two_button.pack(side=LEFT)
    step_three_button = Button(topFrame, text="Step Three", fg='green',
                               command=lambda: console.Step_Three("Step_Three.csv"))
    step_three_button.pack(side=LEFT)
    step_four_button = Button(topFrame, text="Step Four", fg='orange', command=menu_GUI)
    step_four_button.pack(side=LEFT)

    root.mainloop()


gui()
