import csv


def matrix_read(file_name):
    """
    Reads the matrix from the filename
    :param file_name:string, the name of the file
    :return:
    """
    f = open(file_name)
    csv_f = csv.reader(f)
    matrix = []
    rows = 0
    for row in csv_f:
        matrix.append(row)
        rows += 1
    columns = len(matrix[0])

    matrix_updated = []
    for i in range(rows):
        matrix_updated.append([int(x) if x != 'Z' else -1 for x in matrix[i]])

    pair = (matrix_updated, rows, columns)
    return pair


def matrix_write(file_name, matrix, rows):
    """
    Reads the matrix
    :param file_name:string, the name of the file
    :param matrix: list of lists of int values
    :param rows:int, the number of rows
    :return:
    """
    with open(file_name, mode='w') as matrix_file:
        matrix_writer = csv.writer(matrix_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(rows):
            matrix_writer.writerow(matrix[i])
