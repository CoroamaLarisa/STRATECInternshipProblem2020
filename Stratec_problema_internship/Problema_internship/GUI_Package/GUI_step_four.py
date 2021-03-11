import tkinter
from tkinter import *

from Architecture_roads.Step_Four_Class import StepFour


def matrix_gui(rows, columns):
    root = tkinter.Tk()
    StepFour(root, rows, columns).pack(side="top", fill="both", expand=True)
    root.mainloop()


def validate_2(value_string):
    """
    Perform input validation.

    Allow only a value that can be converted to an integer

    """
    if value_string.isdigit():
        return True
    else:
        return False


def menu_GUI():
    root = Tk()

    label_rows = Label(root, text="Number of rows")

    label_columns = Label(root, text="Number of columns")

    label_rows.grid(row=0, sticky=E)

    label_columns.grid(row=1, sticky=E)
    vcmd = root.register(validate_2)

    entry_1 = Entry(root)
    entry_1.grid(row=0, column=1)
    entry_1.config(validate='key', validatecommand=(vcmd, '%P'))

    entry_2 = Entry(root)
    entry_2.grid(row=1, column=1)
    entry_2.config(validate='key', validatecommand=(vcmd, '%P'))

    do_matrix = Button(root, text="Submit",
                       command=lambda: matrix_gui(int(entry_1.get()), int(entry_2.get())))
    do_matrix.grid(columnspan=2)
    root.mainloop()
