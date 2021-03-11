import tkinter as tk

import matplotlib.pyplot as plt

from Architecture_roads.Architecture_matrix import Architecture_matrix
from Service.Service import Service


class SimpleTableInput(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)

        self._entry = {}
        self.rows = rows
        self.columns = columns

        # register a command to use for validation
        vcmd = (self.register(self._validate), '%P')

        # create the table of widgets
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column)
                e = tk.Entry(self, validate="key", validatecommand=vcmd)
                e.grid(row=row, column=column, stick="nsew")
                self._entry[index] = e
        # adjust column weights so they all expand equally
        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)
        # designate a final, empty row to fill up any extra space

    def get_matrix(self):
        """
        Return a list of lists, containing the data in the table
        """
        result = []
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                index = (row, column)
                value = self._entry[index].get()
                if value == "":
                    current_row.append(0)
                elif value == 'Z':
                    current_row.append(-1)
                else:
                    current_row.append(int(value))
            result.append(current_row)
        return result

    def _validate(self, value_string):
        """
        Perform input validation.

        Allow only an empty value, pin Z or a value that can be converted to an integer
        """

        if value_string.strip() == "" or value_string == 'Z':
            return True
        try:
            i = int(value_string)
        except ValueError:
            self.bell()
            return False
        return True


class StepFour(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)
        self.frows = rows
        self.fcolumns = columns
        self.table = SimpleTableInput(self, rows, columns)
        self.submit = tk.Button(self, text="Submit", command=self.on_submit)
        self.table.pack(side="top", fill="both", expand=True)
        self.submit.pack(side="bottom")

    def on_submit(self):
        matrix = self.table.get_matrix()
        architecture = Architecture_matrix(matrix, self.frows, self.fcolumns)
        service = Service(architecture)
        service.show_road_point()
        service.represent_roads()
        self.draw(matrix)

    def draw(self, matrix):
        cmap = 'rainbow'
        plt.matshow(matrix, cmap=cmap)
        plt.title(" Resulted Matrix ")
        plt.show()
