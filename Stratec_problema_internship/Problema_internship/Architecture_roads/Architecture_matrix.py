from Architecture_roads.Cell import Cell


class Architecture_matrix:
    def __init__(self, matrix, rows, columns):
        self.__matrix = matrix
        self.__rows = rows
        self.__columns = columns
        self.__boundaries = {}

    def cell_points(self):
        """
       Asta returneaza dictionar cu points unde cheile sunt nodurile din matrice si valorile sunt coordonatele in care se gasesc
       :return:
       """
        list_points = {}
        for i in range(self.__rows):
            for j in range(len(self.__matrix[1])):
                c = Cell(i, j)
                if self.__matrix[i][j] != 0 and (self.__matrix[i][j] not in list_points):
                    list_points[self.__matrix[i][j]] = []
                    list_points[self.__matrix[i][j]].append(c)
                elif self.__matrix[i][j] in list_points and self.__matrix[i][j] != 0:
                    list_points[self.__matrix[i][j]].append(c)

        return list_points

    def matrix_rows(self):
        return self.__rows

    def matrix_columns(self):
        return self.__columns

    def show(self, list):
        for i in range(len(list)):
            print(list[i])

    def set_x_y(self, x, y, point):
        self.__matrix[x][y] = point
