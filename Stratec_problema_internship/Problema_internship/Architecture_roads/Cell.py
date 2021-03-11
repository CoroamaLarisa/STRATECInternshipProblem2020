class Cell:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        # self.__distance = distance
        # self.__prev = prev

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def boundary(self):
        """
        Returns cell's boundary
        :param x:
        :param y:
        :return:
        """
        return_list = [Cell(self.__x + 1, self.__y - 1), Cell(self.__x + 1, self.__y), Cell(self.__x + 1, self.__y + 1),
                       Cell(self.__x, self.__y - 1), Cell(self.__x, self.__y), Cell(self.__x, self.__y + 1),
                       Cell(self.__x - 1, self.__y - 1),
                       Cell(self.__x - 1, self.__y), Cell(self.__x - 1, self.__y + 1)]
        return return_list

    def __eq__(self, other):
        return self.__x == other.get_x() and self.__y == other.get_y()

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return f'"The x coordinate is " {self.get_x()} ,"The y coordinate is " {self.get_y()}'

