class Road:
    def __init__(self, st_cell, ed_cell):
        self.__st_cell = st_cell
        self.__ed_cell = ed_cell
        self.__road = []

    def add_cell(self, cell):
        self.__road.append(cell)

    def start_cell(self):
        return self.__st_cell

    def end_cell(self):
        return self.__ed_cell

    def set_road(self, list):
        if not list:
            self.__road.clear()
        else:
            for cell in list:
                self.__road.append(cell)

    def previous_cell(self):
        return self.__road[-1]

    def get_road(self):
        return self.__road

    def __eq__(self, other):
        if not isinstance(other, Road):
            return False
        else:
            return self.__st_cell == other.start_cell() and self.__ed_cell == other.end_cell() and \
                   self.__road == other.get_road()

    def __ne__(self, other):
        return not (self == other)

    def respect_self_boundary(self, cell, cell_prev):
        """
        Verificam daca celula pe care vrem sa o adaugam se afla intr-un loc interzis
        Daca va avea alt vecin inafara de ultima celula atunci acest drum nu se poate forma
        :param cell: Celula pe care o verificam
        :param cell_prev: Ultima celula din drum
        :return: True respecta restrictia/False daca nu
        """
        for cell_list in self.__road:
            if cell_list != cell_prev:
                if cell.get_x() - 1 == cell_list.get_x() and cell.get_y() == cell_list.get_y():
                    return False
                elif cell.get_x() + 1 == cell_list.get_x() and cell.get_y() == cell_list.get_y():
                    return False
                elif cell.get_y() + 1 == cell_list.get_y() and cell.get_x() == cell_list.get_x():
                    return False
                elif cell.get_y() - 1 == cell_list.get_y() and cell.get_x() == cell_list.get_x():
                    return False

        return True
        # if axis == 1:
        #     if Cell(cell.get_x(), cell.get_y()+1) in self.__road:
        #         return False
        # elif axis == 2:
        #     if Cell(cell.get_x()-1,cell.get_y())in self.__road:
        #         return False
        # elif axis == -1:
        #     if Cell(cell.get_x(), cell.get_y()-1) in self.__road:
        #         return False
        # elif axis == -2:
        #     if Cell(cell.get_x()+1, cell.get_y()) in self.__road:
        #         return False
        # return True

    def __str__(self):
        return ",".join([str(c) for c in self.__road])

# def add_self_boundary(self, point, cell):
#     """
#     Auga
#     :param point:
#     :param cell:
#     :return:
#     """
#     new_boundary = cell.boundary()
#     for tuple in new_boundary:
#         if tuple not in self.__boundary[point]:
#             self.__boundary[point].append(tuple)
