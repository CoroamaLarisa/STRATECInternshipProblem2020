from Architecture_roads.Architecture_matrix import Architecture_matrix
from Architecture_roads.Read_Write import matrix_read, matrix_write
from Service.Service import Service
import matplotlib.pyplot as plt


class Console:

    def Step_One(self,file_name_in,file_name_out):
        pair = matrix_read(file_name_in)
        matrix = pair[0]
        rows = pair[1]
        columns = pair[2]
        architecture = Architecture_matrix(matrix, rows, columns)
        service = Service(architecture)
        service.show_road_point()
        service.represent_roads()
        matrix_write(file_name_out, matrix, rows)
        self.show_matrix(matrix)

    def Step_Two(self,file_name_in,file_name_out):
        pair = matrix_read(file_name_in)
        matrix = pair[0]
        rows = pair[1]
        columns = pair[2]
        architecture = Architecture_matrix(matrix, rows, columns)
        service = Service(architecture)
        service.show_road_point()
        service.represent_roads()
        matrix_write(file_name_out, matrix, rows)
        self.show_matrix(matrix)

    def Step_Three(self,file_name_in):
        pair = matrix_read(file_name_in)
        matrix = pair[0]
        rows = pair[1]
        columns = pair[2]
        architecture = Architecture_matrix(matrix, rows, columns)
        service = Service(architecture)
        service.represent_points()
        self.show_matrix(matrix)

    def show_matrix(self, matrix):
        cmap = 'rainbow'
        plt.matshow(matrix, cmap=cmap)
        plt.title("Resulted Matrix")
        plt.show()
