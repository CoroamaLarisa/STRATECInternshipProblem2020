from Architecture_roads.Cell import Cell
from Architecture_roads.Roads import Road


class Service:
    def __init__(self, architecture):
        self.__boundaries = {}
        self.__roads = {}
        self.__roads_per_point = {}
        self.__possible_roads_to_take = {}
        self.__architecture = architecture
        self.__road_in_undo = []
        self.__remaining_values = []
        self.initial_boundary()
        self.initial_roads()
        self.initial_possible_roads()
        self.__switch = 0

    def initial_roads(self):
        """
        Initializing the roads for each point
        :return:
        """
        points_cells = self.__architecture.cell_points()
        for point in points_cells.keys():
            self.__roads_per_point[point] = []

    def initial_boundary(self):
        """
        Initializing the boundaries so each point has the boundaries of their cells
        :return:
        """
        points_cells = self.__architecture.cell_points()
        for point in points_cells.keys():
            self.__boundaries[point] = []
            for cell in points_cells[point]:
                c = cell.boundary()
                for cell in c:
                    if cell not in self.__boundaries[point]:
                        self.__boundaries[point].append(cell)

    def initial_possible_roads(self):
        """
        Initializing the possible roads for each point
        :return:
        """
        cell_points = self.__architecture.cell_points()
        for point in cell_points:
            if point != -1:
                self.__possible_roads_to_take[point] = []

    def add_forbidden_boundary(self, point, cell):
        """
        Adds the boundary of the imputed cell in the list with boundaries of the point
        :param point: int
        :param cell: the cell of which we have to add the boundary
        :return:
        """
        new_boundary = cell.boundary()
        for cell in new_boundary:
            if cell not in self.__boundaries[point]:
                self.__boundaries[point].append(cell)

    def respects_forbidden_boundary(self, point, cell):
        """
        Verifies if a cell respects the boundaries of the other roads
        :param point: the value of whose road has the cell
        :param cell: the cell that we want to verify
        :return: True if it respects/False if not
        """
        for key in self.__boundaries.keys():
            if key != point:
                for cell_2 in self.__boundaries[key]:
                    if cell == cell_2:
                        return False
        return True

    def deletes_first_cell(self, cell_list, point):
        """
        :param cell_list: list of cells
        :param point: int
        :return:
        """
        for i in range(len(cell_list[point]) - 1):
            cell_list[point][i] = cell_list[point][i + 1]
        if len(cell_list[point]) >= 1:
            cell_list[point].pop()

    def delete_from_boundary(self, point, list_to_add):
        """
        Deletes from the list of boundaries of the point the list in the parameters
        :param point: the point
        :param list_to_add: the list to be deleted
        :return:
        """
        list_untouched = []
        cell_point = self.__architecture.cell_points()
        for cell_interm in cell_point[point]:
            for cell_b in cell_interm.boundary():
                if cell_b not in list_untouched:
                    list_untouched.append(cell_b)

        new_list = []
        for cell in self.__boundaries[point]:
            allow = 0
            if cell in list_untouched:
                new_list.append(cell)
                continue
            for cell_1 in list_to_add:
                for cell_2 in cell_1.boundary():
                    if cell == cell_2:
                        allow = 0
            if allow == 1:
                new_list.append(cell)
        self.__boundaries[point].clear()
        self.__boundaries[point] = new_list[::]

    def delete_road(self, point, list_cells, op):
        """
        Deletes the road from the list of roads of the point
        :param point:
        :param list_cells:
        :param op:
        :return:
        """
        for i in range(len(self.__roads_per_point[point]) - 1):
            if self.__roads_per_point[point][i].get_road() == list_cells:
                self.__roads_per_point[point][i] = self.__roads_per_point[point][
                    i + 1]

        self.__roads[point].set_road([])
        if (op == 1) and len(self.__roads_per_point[point]) >= 1:
            self.__roads_per_point[point].pop()

    def erases_from_possible_roads(self, point, road):
        """
        It erases a specified road from the list of possible roads for a value
        :param point: the value
        :param road: the road that we wish to erase
        :return:
        """
        for i in range(len(self.__possible_roads_to_take[point])):
            if self.__possible_roads_to_take[point][i] == road:
                for j in range(i, len(self.__possible_roads_to_take[point]) - 1):
                    self.__possible_roads_to_take[point][j].set_road(
                        self.__possible_roads_to_take[point][j + 1].get_road())

        self.__possible_roads_to_take[point].pop()

    def clear_possible_roads(self, point):
        """
        Clears all possible roads
        :param point:
        :return:
        """
        self.__possible_roads_to_take[point].clear()

    def undo(self, point_next):
        """
        Goes through all the possible roads of the previous point so that both the road for the point and the
        road for the previous point can be made.If there is no possible option , it completely deletes the previous road
        :param point_next: the point
        :return:
        """
        if len(self.__road_in_undo) >= 1:
            tuple = self.__road_in_undo.pop()
            list_cells = tuple[0]
            point = tuple[1]
            cell_start = self.__roads[point_next].start_cell()
            cell_end = self.__roads[point_next].end_cell()
            self.delete_road(point, list_cells, 1)
            self.delete_from_boundary(point, list_cells)
            while len(self.__possible_roads_to_take[point]) >= 1:
                road = self.__possible_roads_to_take[point][0]
                self.erases_from_possible_roads(point, road)
                self.add_boundaries_list(point, road.get_road())
                list_road = self.many_roads(point, cell_start, cell_end)
                self.add_to_possible_roads(point_next, list_road)
                result = self.if_a_road_can_be_taken(point_next)
                if len(result.get_road()) >= 3:
                    self.add_boundaries_list(point, road.get_road())
                    self.__road_in_undo.append((road.get_road(), point))
                    self.__road_in_undo.append((result.get_road(), point_next))
                    self.__roads_per_point[point].append(self.__roads[point])
                    self.__roads_per_point[point_next].append(self.__roads[point_next])
                else:
                    self.delete_road(point, road.get_road(), 0)
                    self.delete_from_boundary(point, road.get_road())
                    self.clear_possible_roads(point_next)
            if len(self.__possible_roads_to_take[point]) == 0:
                self.__possible_roads_to_take[point].clear()
                if point not in self.__remaining_values:
                    self.__remaining_values.append(point)
        else:
            return 0

    def find_if_next_point_has_values(self, point):
        """
        Verifies if there is a road for the next point
        :param point: the point
        :return: the point if there is a road / o if there is not
        """
        cell_points = self.__architecture.cell_points()
        i = 0
        point_find = 0
        result = 0
        for point_2 in cell_points.keys():
            i += 1
            if point_2 == point:
                result = i
        i = 0
        for point_2 in cell_points.keys():
            i += 1
            if result + 1 == i:
                point_find = point_2

        if point_find != 0:
            if len(self.__roads_per_point[point_find]) >= 1:
                return point_find
        return 0

    def get_previous_point(self, point):
        """
        Returns the previous point of the point in the parameters
        :param point: the point
        :return: the previous_point
        """
        cell_points = self.__architecture.cell_points()
        i = 0
        point_find = 0
        result = 0
        for point_2 in cell_points.keys():
            i += 1
            if point_2 == point:
                result = i
        i = 0
        for point_2 in cell_points.keys():
            i += 1
            if result - 1 == i:
                point_find = point_2

        return point_find

    def get_next_point(self, point):
        """
        Returns the previous point of the point in the parameters
        :param point: the point
        :return: the previous_point
        """
        cell_points = self.__architecture.cell_points()
        i = 0
        point_find = 0
        result = 0
        for point_2 in cell_points.keys():
            i += 1
            if point_2 == point:
                result = i
        i = 0
        for point_2 in cell_points.keys():
            i += 1
            if result + 1 == i:
                point_find = point_2

        return point_find

    def in_between_remaining_points(self, point, previous_point):
        """
        Inserts the given point in from of the previous_point from  the parameters
        :param point: the point
        :param previous_point: the previous point
        :return:
        """
        new_list = []
        for i in range(len(self.__remaining_values)):
            if self.__remaining_values[i] == previous_point:
                new_list.append(previous_point)
                new_list.append(point)
            else:
                new_list.append(self.__remaining_values[i])

        self.__remaining_values.clear()
        for x in new_list:
            self.__remaining_values.append(x)

    def deletes_from_remaining_points(self, point):
        """
        Deletes a point from the remaining points
        :param point:
        :return:
        """
        for i in range(len(self.__remaining_values) - 1):
            if self.__remaining_values[i] == point:
                for j in range(i, len(self.__remaining_values) - 1):
                    self.__remaining_values[i] = self.__remaining_values[i + 1]
        self.__remaining_values.pop()

    def if_both_roads_can_be_made(self, previous_point, next_point, list_to_add, point):
        """
        :param point:
        :param list_to_add:
        :param next_point: 10 pt noi
        :param previous_point: 8 pt noi
        :return:
        """
        cell_points = self.__architecture.cell_points()
        cell_start_2 = cell_points[next_point][0]
        cell_end_2 = cell_points[next_point][1]
        list_roads_2 = self.many_roads(next_point, cell_start_2, cell_end_2)
        self.add_to_possible_roads(point, list_roads_2)
        result_2 = self.if_a_road_can_be_taken(next_point)
        if result_2.get_road():
            self.add_boundaries_list(next_point, result_2.get_road())
            self.erases_from_possible_roads(next_point, result_2.get_road())
        cell_start = cell_points[previous_point][0]
        cell_end = cell_points[previous_point][1]
        list_roads = self.many_roads(previous_point, cell_end, cell_start)
        self.add_to_possible_roads(previous_point, list_roads)
        result = self.if_a_road_can_be_taken(previous_point)
        if result.get_road():
            self.add_boundaries_list(previous_point, result.get_road())
            self.erases_from_possible_roads(previous_point, result)
        if result.get_road() and result_2.get_road():
            self.__road_in_undo.append((result, previous_point))
            self.__road_in_undo.append((list_to_add, point))
            self.__road_in_undo.append((result_2, next_point))
            self.__roads_per_point[previous_point].append(self.__roads[previous_point])
            self.deletes_first_cell(cell_points, previous_point)
            self.__roads_per_point[next_point].append(self.__roads[next_point])
            self.deletes_first_cell(cell_points, next_point)
            self.__roads_per_point[point].append(self.__roads[point])
            self.deletes_first_cell(cell_points, point)
            self.deletes_from_remaining_points(next_point)
            self.deletes_from_remaining_points(previous_point)
            return True
        else:
            self.__roads[previous_point].set_road([])
            self.delete_from_boundary(previous_point, result.get_road())
            self.__roads[next_point].set_road([])
            self.delete_from_boundary(next_point, result_2.get_road())
            self.clear_possible_roads(previous_point)
            self.clear_possible_roads(next_point)
            return False

    def if_point_can_have_road(self, point):
        """
        Verifies if a point can have a road
        :param point:
        :return: True if it can/False if it can't
        """
        cell_points = self.__architecture.cell_points()
        cell_start = cell_points[point][0]
        cell_end = cell_points[point][1]
        result = self.build_road(point, cell_end, [cell_start])
        if result:
            return True
        return False

    def final_many_roads(self, point, cell_start, cell_end):
        """
        Finds the first road that isn't empty by using the main function
        or adding additional Cells to it so other roads can be formed
        :param point:int, the point
        :param cell_start:Cell, the stars that starts
        :param cell_end: Cell, the destination of the road
        :return: a road or an empty list

        """
        self.__roads[point] = Road(cell_start, cell_end)
        self.__roads[point].add_cell(cell_start)
        list_cells = [cell_start]
        list_cells = self.build_road(point, cell_end, list_cells)

        if list_cells:
            road_main = Road(cell_start, cell_end)
            road_main.set_road(list_cells)
            return road_main

        road_up_right = self.road_1(point, cell_start, [cell_start])
        if len(road_up_right) > 0:
            list_cells_2 = self.build_road(point, cell_end, [cell_start] + road_up_right)
            if list_cells_2:
                road_2 = Road(cell_start, cell_end)
                road_2.set_road(list_cells_2)
                return road_2

        road_up_left = self.road_2(point, cell_start, [cell_start])
        if len(road_up_left) > 0:
            list_cells_3 = self.build_road(point, cell_end, [cell_start] + road_up_left)
            if list_cells_3:
                road_3 = Road(cell_start, cell_end)
                road_3.set_road(list_cells_3)
                return road_3

        road_down_right = self.road_3(point, cell_start, [cell_start])
        if len(road_down_right) > 0:
            list_cells_4 = self.build_road(point, cell_end, [cell_start] + road_down_right)
            if list_cells_4:
                road_4 = Road(cell_start, cell_end)
                road_4.set_road(list_cells_4)
                return road_4

        road_down_left = self.road_4(point, cell_start, [cell_start])
        if len(road_down_left) > 0:
            list_cells_5 = self.build_road(point, cell_end, [cell_start] + road_down_left)
            if list_cells_5:
                road_5 = Road(cell_start, cell_end)
                road_5.set_road(list_cells_5)
                return road_5

        return []

    def many_roads(self, point, cell_start, cell_end):
        """
        Finds a maximum of 5 roads that can be done from the cell stars to the cell_end
        :param point:int
        :param cell_start: the first cell
        :param cell_end: the destination cell
        :return: a list of roads that can be made
        """
        self.__roads[point] = Road(cell_start, cell_end)
        self.__roads[point].add_cell(cell_start)
        x = cell_start.get_x()
        y = cell_start.get_y()
        list_roads = []
        list_cells = [cell_start]
        list_cells = self.build_road(point, cell_end, list_cells)
        if list_cells:
            road_main = Road(cell_start, cell_end)
            road_main.set_road(list_cells)
            list_roads.append(road_main)

        road_up_right = self.up_and_right(point, cell_start, [cell_start])
        if len(road_up_right) > 0:
            list_cells_2 = self.build_road(point, cell_end, [cell_start] + road_up_right)
            if list_cells_2:
                road_2 = Road(cell_start, cell_end)
                road_2.set_road(list_cells_2)
                list_roads.append(road_2)

        road_up_left = self.up_and_left(point, cell_start, [cell_start])
        if len(road_up_left) > 0:
            list_cells_3 = self.build_road(point, cell_end, [cell_start] + road_up_left)
            if list_cells_3:
                road_3 = Road(cell_start, cell_end)
                road_3.set_road(list_cells_3)
                list_roads.append(road_3)

        road_down_right = self.down_and_right(point, cell_start, [cell_start])
        if len(road_down_right) > 0:
            list_cells_4 = self.build_road(point, cell_end, [cell_start] + road_down_right)
            if list_cells_4:
                road_4 = Road(cell_start, cell_end)
                road_4.set_road(list_cells_4)
                list_roads.append(road_4)

        road_down_left = self.down_and_left(point, cell_start, [cell_start])
        if len(road_down_left) > 0:
            list_cells_5 = self.build_road(point, cell_end, [cell_start] + road_down_left)
            if list_cells_5:
                road_5 = Road(cell_start, cell_end)
                road_5.set_road(list_cells_5)
                list_roads.append(road_5)

        return list_roads

    def if_a_road_can_be_taken(self, point):
        """
        Verifies if a point has a road that can be taken
        :return:a road
        """
        road = Road(self.__roads[point].start_cell(), self.__roads[point].end_cell())
        if len(self.__possible_roads_to_take[point]) == 0:
            road.set_road([])
            return road
        road = Road(self.__possible_roads_to_take[point][0].start_cell(),
                    self.__possible_roads_to_take[point][0].end_cell())
        road.set_road(self.__possible_roads_to_take[point][0].get_road())
        if len(self.__possible_roads_to_take[point]) > 1:
            for j in range(len(self.__possible_roads_to_take[point]) - 1):
                self.__possible_roads_to_take[point][j].set_road(self.__possible_roads_to_take[point][j + 1].get_road())
        self.__possible_roads_to_take[point].pop()
        return road

    def add_to_possible_roads(self, point, list_roads):
        """
        Adds a road to the possible roads of a point
        :param point:
        :param list_roads: the list of the road added
        :return:
        """
        if len(self.__possible_roads_to_take[point]) >= 1:
            self.__possible_roads_to_take[point].clear()
        for road in list_roads:
            self.__possible_roads_to_take[point].append(road)

    def fast_undo(self):
        """
        Makes an undo , which deletes the previous road
        :return:
        """
        if len(self.__road_in_undo) >= 1:
            tuple = self.__road_in_undo.pop()
            list_cells = tuple[0]
            point = tuple[1]
            self.delete_road(point, list_cells, 1)
            self.delete_from_boundary(point, list_cells)
            if point not in self.__remaining_values:
                self.__remaining_values.append(point)

    def neighbours_undo(self, point, next_point):
        """
        Deletes the roads from the neighbour points
        :param point: the previous_point from cell_points
        :param next_point: the next_point from cell_points
        :return:
        """
        road = self.__roads[next_point]
        list_cells = road.get_road()
        self.delete_road(next_point, list_cells, 1)
        self.delete_from_boundary(next_point, list_cells)
        self.clear_possible_roads(next_point)
        if next_point not in self.__remaining_values:
            self.__remaining_values.append(next_point)

        self.__road_in_undo.pop()
        road = self.__roads[point]
        list_cells = road.get_road()
        self.delete_road(point, list_cells, 1)
        self.delete_from_boundary(point, list_cells)
        if point not in self.__remaining_values:
            self.__remaining_values.append(point)
        self.clear_possible_roads(point)

    def can_make_roads(self, cell_points):
        """
        Makes a combination of roads so that they can fit perfectly
        :param cell_points:
        :return:
        """
        first_point = self.__remaining_values[0]
        cell_start = self.__roads[first_point].start_cell()
        cell_end = self.__roads[first_point].end_cell()
        list_roads = self.many_roads(first_point, cell_start,
                                     cell_end)
        i = 0
        for road_main in list_roads:
            i += 1
            self.add_boundaries_list(first_point, road_main.get_road())
            cell_start_2 = self.__roads[self.__remaining_values[1]].start_cell()
            cell_end_2 = self.__roads[self.__remaining_values[1]].end_cell()
            list_road_point_2 = self.many_roads(self.__remaining_values[1], cell_start_2, cell_end_2)
            for road_2 in list_road_point_2:
                self.add_boundaries_list(self.__remaining_values[1], road_2.get_road())
                cell_start_3 = self.__roads[self.__remaining_values[2]].start_cell()
                cell_end_3 = self.__roads[self.__remaining_values[2]].end_cell()
                list_road_point_3 = self.many_roads(self.__remaining_values[2], cell_start_3, cell_end_3)
                for road_3 in list_road_point_3:
                    self.add_boundaries_list(self.__remaining_values[2], road_3.get_road())
                    cell_start_4 = self.__roads[self.__remaining_values[3]].start_cell()
                    cell_end_4 = self.__roads[self.__remaining_values[3]].end_cell()
                    road_4 = self.final_many_roads(self.__remaining_values[3], cell_start_4, cell_end_4)

                    if road_4:
                        self.add_boundaries_list(self.__remaining_values[3], road_4.get_road())
                        for point in self.__remaining_values:
                            self.__road_in_undo.append((self.__roads[point].get_road(), point))
                            self.__roads_per_point[point].append(self.__roads[point])
                            self.deletes_first_cell(cell_points, point)
                        self.__remaining_values.clear()
                        return True

                    self.__possible_roads_to_take[self.__remaining_values[3]].clear()
                    self.delete_road(self.__remaining_values[2], road_3.get_road(), 0)
                    self.delete_from_boundary(self.__remaining_values[2], road_3.get_road())
                self.delete_road(self.__remaining_values[1], road_2.get_road(), 0)
                self.delete_from_boundary(self.__remaining_values[1], road_2.get_road())
            self.delete_road(first_point, road_main.get_road(), 0)
            self.delete_from_boundary(first_point, road_main.get_road())

        return False

    def multiple_undo(self, previous_point):
        """
        Does multiple undos for a point that has many roads
        :param previous_point:
        :return:
        """
        while self.__roads_per_point[previous_point]:
            self.fast_undo()

    def building_road(self, point, list_condition):
        """
        Builds a road for a value
        :param list_condition:
        :param point: the value
        :return:
        """
        list_condition[0] = 1
        list_condition[1] = 1
        cell_points = self.__architecture.cell_points()
        for cell in cell_points[point]:
            if not self.respects_forbidden_boundary(point, cell):
                raise ValueError("You introduced a number in another's boundary")

        cell_start = cell_points[point][0]
        cell_end = cell_points[point][1]
        self.__roads[point] = Road(cell_start, cell_end)
        self.__roads[point].add_cell(cell_start)
        road = self.final_many_roads(point, cell_start, cell_end)
        if road != []:
            road = road.get_road()
        if road:
            self.add_boundaries_list(point, road)
            self.__road_in_undo.append((road, point))
            self.__roads_per_point[point].append(self.__roads[point])
            self.deletes_first_cell(cell_points, point)
        else:
            while not road and list_condition[1]:
                result = self.find_if_next_point_has_values(point)
                if result != 0 and self.__switch != 1:
                    next_point = self.get_next_point(point)
                    previous_point = self.get_previous_point(point)
                    self.neighbours_undo(previous_point, next_point)
                    list_roads = self.many_roads(point, cell_start, cell_end)
                    self.add_to_possible_roads(point, list_roads)
                    while len(self.__possible_roads_to_take[point]) >= 1 and list_condition[1]:
                        result = self.if_a_road_can_be_taken(point)
                        self.__switch = 1
                        if len(result.get_road()) >= 3:
                            self.add_boundaries_list(point, result.get_road())
                            self.__road_in_undo.append((result.get_road(), point))
                            next_point = self.get_next_point(point)
                            previous_point = self.get_previous_point(point)
                            if self.__switch == 1 and not self.if_both_roads_can_be_made(previous_point,
                                                                                         next_point,
                                                                                         result.get_road(),
                                                                                         point):

                                self.in_between_remaining_points(point, next_point)
                                self.fast_undo()
                                self.fast_undo()
                                if self.can_make_roads(cell_points):
                                    self.__remaining_values.clear()
                                    list_condition[1] = 0
                                    list_condition[0] = 0

                                if len(self.__possible_roads_to_take[point]) == 0:
                                    list_condition[1] = 0
                                list_condition[0] = 0

                else:
                    self.undo(point)
                    list_roads = self.many_roads(point, cell_start, cell_end)
                    self.add_to_possible_roads(point, list_roads)
                    road = self.if_a_road_can_be_taken(point)
                    if len(road.get_road()) >= 3:
                        self.add_boundaries_list(point, road.get_road())
                        self.__roads_per_point[point].append(self.__roads[point])
                        self.deletes_first_cell(cell_points, point)
                        self.__switch = 0
                    else:
                        road = []

        while len(self.__remaining_values) >= 1:
            point_new = self.__remaining_values[0]
            for i in range(len(self.__remaining_values) - 1):
                self.__remaining_values[i] = self.__remaining_values[i + 1]
            self.__remaining_values.pop()
            self.building_road(point_new, list_condition)

    def undo_many_roads(self):
        tuple = self.__road_in_undo[-1]
        point = tuple[1]
        self.multiple_undo(point)

    def building_road_for_multiple(self, point):
        """
        Builds a road for a point with more than three cells that have that point
        :param point:
        :return:
        """
        cell_points = self.__architecture.cell_points()
        list_roads = []
        n = len(self.__roads_per_point[point])

        for j in range(0, len(cell_points[point]) - 1):
            already_in = 1
            for road in list_roads:
                if cell_points[point][j + 1] in road.get_road():
                    already_in = 0
            if already_in:
                road = self.final_many_roads(point, cell_points[point][j], cell_points[point][j + 1])
                if road:
                    list_roads.append(road)
                    n += 1
                    if n == len(cell_points[point]) - 1:
                        break
                else:
                    while not road:
                        self.undo_many_roads()
                        road = self.final_many_roads(point, cell_points[point][j], cell_points[point][j + 1])
                        if road:
                            list_roads.append(road)

        for road in list_roads:
            self.__roads[point] = Road(road.start_cell(), road.end_cell())
            self.add_boundaries_list(point, road.get_road())
            self.__roads_per_point[point].append(road)
            self.__road_in_undo.append((road.get_road(), point))

        while len(self.__remaining_values) >= 1:
            point_new = self.__remaining_values[0]
            for i in range(len(self.__remaining_values) - 1):
                self.__remaining_values[i] = self.__remaining_values[i + 1]
            self.__remaining_values.pop()
            self.building_road_for_multiple(point_new)

    def build_road(self, point, cell_end, list_cells):
        """
        Builds road for point
        :param point: point
        :param cell_end: the ending cell
        :param list_cells: the list of cells (which in itself is a road but isn't initialized as a Road yet)
        :return: the list of cells of an empty list of a road can't be made
        """

        current_cell = list_cells[-1]
        x, y = current_cell.get_x(), current_cell.get_y()

        if x == cell_end.get_x() and y == cell_end.get_y():
            return list_cells

        end_x = cell_end.get_x()
        end_y = cell_end.get_y()
        ok = self.verifies_if_there_is_something_in_the_path_until_same_x(point, list_cells[-1], cell_end)
        if ok and y == cell_end.get_y():
            if self.build_road_to_until_x(list_cells[-1], cell_end.get_x(), list_cells):
                return list_cells

        if self.verifies_if_there_is_something_in_the_path_until_same_y(point, list_cells[-1],
                                                                        cell_end) and x == cell_end.get_x():
            if self.build_road_to_until_y(list_cells[-1], cell_end.get_y(), list_cells):
                return list_cells

        firstCell = Cell(end_x, y)
        secondCell = Cell(x, end_y)

        if self.respects_forbidden_boundary(point, firstCell) and \
                self.verifies_if_there_is_something_in_the_path_until_same_x(point, list_cells[-1], firstCell) \
                and self.verifies_if_there_is_something_in_the_path_until_same_y(point, firstCell, cell_end):
            if self.build_road_to_until_x(list_cells[-1], firstCell.get_x(), list_cells) and \
                    self.build_road_to_until_y(firstCell, cell_end.get_y(), list_cells):
                return list_cells

        if self.respects_forbidden_boundary(point, secondCell) and \
                self.verifies_if_there_is_something_in_the_path_until_same_x(point, secondCell, cell_end) \
                and self.verifies_if_there_is_something_in_the_path_until_same_y(point, list_cells[-1],
                                                                                 secondCell):
            if self.build_road_to_until_y(list_cells[-1], secondCell.get_y(), list_cells) and \
                    self.build_road_to_until_x(secondCell, cell_end.get_x(), list_cells):
                return list_cells

        if self.road_through_two_branches_up(point, list_cells[-1], cell_end, list_cells):
            return list_cells
        elif self.road_through_two_branches_down(point, list_cells[-1], cell_end, list_cells):
            return list_cells
        elif self.road_through_two_branches_right(point, list_cells[-1], cell_end, list_cells):
            return list_cells
        elif self.road_through_two_branches_left(point, list_cells[-1], cell_end, list_cells):
            return list_cells
        else:
            if (x >= cell_end.get_x() and Cell(x - 1, y) not in list_cells) or (
                    x <= cell_end.get_x() and not ok and Cell(x - 1, y) not in list_cells) \
                    or (x <= cell_end.get_x() and (x == end_x - 1) and Cell(x - 1, y) not in list_cells):

                if y >= cell_end.get_y():
                    road_up_left = self.up_and_left(point, list_cells[-1], list_cells)
                    if len(road_up_left) == 0:
                        road_up_right = self.up_and_right(point, list_cells[-1], list_cells)
                        if len(road_up_right) != 0:
                            return self.build_road(point, cell_end, list_cells + road_up_right)
                    else:
                        return self.build_road(point, cell_end, list_cells + road_up_left)
                else:
                    road_up_right = self.up_and_right(point, list_cells[-1], list_cells)
                    if len(road_up_right) == 0:
                        road_up_left = self.up_and_left(point, list_cells[-1], list_cells)
                        if len(road_up_left) != 0:
                            return self.build_road(point, cell_end, list_cells + road_up_left)
                    else:
                        return self.build_road(point, cell_end, list_cells + road_up_right)
            else:
                if y >= cell_end.get_y():
                    road_down_left = self.down_and_left(point, list_cells[-1], list_cells)
                    if len(road_down_left) != 0:
                        return self.build_road(point, cell_end, list_cells + road_down_left)
                    else:
                        road_down_right = self.down_and_right(point, list_cells[-1], list_cells)
                        if len(road_down_right) != 0:
                            return self.build_road(point, cell_end, list_cells + road_down_right)
                else:
                    road_down_right = self.down_and_right(point, list_cells[-1], list_cells)
                    if len(road_down_right) != 0:
                        return self.build_road(point, cell_end, list_cells + road_down_right)
                    else:
                        road_down_left = self.down_and_left(point, list_cells[-1], list_cells)
                        if len(road_down_left) != 0:
                            return self.build_road(point, cell_end, list_cells + road_down_left)

        return []

    def verifies_if_there_is_something_in_the_path_until_same_y(self, point_p, cell_st, cell_end):
        """
        Verifies if there are other cells other than the ones with the same value point
        If the path is safe or not
        :param cell_end:
        :param cell_st:
        :param point_p: the value of the cell
        :return: True if it is safe / False if it isn't
        """
        x = cell_st.get_x()
        y = cell_st.get_y()
        end_y = cell_end.get_y()
        if y < end_y:
            y += 1
        elif y > end_y:
            y -= 1
        else:
            return False

        while y != end_y:
            if not self.respects_forbidden_boundary(point_p, Cell(x, y)):
                return False
            if y < end_y:
                y += 1
            elif y > end_y:
                y -= 1

        return True

    def verifies_if_there_is_something_in_the_path_until_same_x(self, point_p, cell_st, cell_end):
        """
        Verifies if there are other cells other than the ones with the same value point
        If the path is safe or not
        :param cell_end:
        :param cell_st:
        :param point_p: the value of the cell
        :return: True if it is safe / False if it isn't
        """
        x = cell_st.get_x()
        y = cell_st.get_y()
        end_x = cell_end.get_x()
        if x < end_x:
            x += 1
        elif x > end_x:
            x -= 1
        else:
            return False
        while x != end_x:
            if not self.respects_forbidden_boundary(point_p, Cell(x, y)):
                return False
            if x < end_x:
                x += 1
            elif x > end_x:
                x -= 1

        return True

    def build_road_to_until_x(self, cell_st, end_x, list_cells):
        """
        Builds a road from the coordinate x until it reaches the coordinate end_x
        :param cell_st: the first cell
        :param end_x: the x coordinate from the ending cell
        :param list_cells: list of cells
        :return: True/False depending if the road can be made
        """
        x = cell_st.get_x()
        y = cell_st.get_y()
        if x < end_x:
            x += 1
            if Cell(x, y) in list_cells:
                return False
            while x <= end_x:
                list_cells.append(Cell(x, y))
                x += 1
        else:
            x -= 1
            if Cell(x, y) in list_cells:
                return False
            while x >= end_x:
                list_cells.append(Cell(x, y))
                x -= 1

        return True

    def build_road_to_until_y(self, cell_st, end_y, list_cells):

        """
        Builds a road from the coordinate y until it reaches the coordinate end_y
        :param cell_st: the first cell
        :param end_y: the y coordinate from the ending cell
        :param list_cells: list of cells
        :return: True/False depending if the road can be made
        """
        x = cell_st.get_x()
        y = cell_st.get_y()
        if y < end_y:
            y += 1
            if Cell(x, y) in list_cells:
                return False
            while y <= end_y:
                list_cells.append(Cell(x, y))
                y += 1
        else:
            y -= 1
            if Cell(x, y) in list_cells:
                return False
            while y >= end_y:
                list_cells.append(Cell(x, y))
                y -= 1

        return True

    def up_and_left(self, point, cell, list_cells):
        """
        Buils a list of cells to the left until it is possible to move down
        or if it not possible to move to the left it moves up until it is possible to move left
        and then moves left until it is possible to move down
        :param point: the point
        :param cell: the current cell
        :param list_cells: the list of cells
        :return: the road of cells resulted
        """
        x = cell.get_x()
        y = cell.get_y()
        road = []
        if y >= 1 and self.respects_forbidden_boundary(point, Cell(x, y - 1)):
            road.append(Cell(x, y - 1))
            y -= 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x + 1, y)):
                    break
                y -= 1
                if y < 0:
                    return []
        elif x >= 1 and self.respects_forbidden_boundary(point, Cell(x - 1, y)):
            road.append(Cell(x - 1, y))
            x -= 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x, y - 1)):
                    break
                x -= 1
                if x < 0:
                    return []
            if y >= 1 and self.respects_forbidden_boundary(point, Cell(x, y - 1)):
                road.append(Cell(x, y - 1))
                y -= 1
                if Cell(x, y) in list_cells:
                    return []
                while self.respects_forbidden_boundary(point, Cell(x, y)):
                    road.append(Cell(x, y))
                    if self.respects_forbidden_boundary(point, Cell(x + 1, y)):
                        break
                    y -= 1
                    if y < 0:
                        return []

        return road

    def up_and_right(self, point, cell, list_cells):
        """
        Buils a list of cells to the right until it is possible to move down
        or if it not possible to move to the right it moves up until it is possible to move right
        and then moves right until it is possible to move down
        :param point: the point
        :param cell: the current cell
        :param list_cells: the list of cells
        :return: the road of cells resulted

        """
        x = cell.get_x()
        y = cell.get_y()
        road = []
        if y < (self.__architecture.matrix_columns() - 1) and self.respects_forbidden_boundary(point, Cell(x, y + 1)):
            road.append(Cell(x, y + 1))
            y += 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x + 1, y)):
                    break
                y += 1
                if y == self.__architecture.matrix_columns():
                    return []
        elif x >= 1 and self.respects_forbidden_boundary(point, Cell(x - 1, y)):
            road.append(Cell(x - 1, y))
            x -= 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x, y + 1)):
                    break
                x -= 1
                if x < 0:
                    return []
            if y < self.__architecture.matrix_columns() - 1 and self.respects_forbidden_boundary(point,
                                                                                                 Cell(x, y + 1)):
                road.append(Cell(x, y + 1))
                y += 1
                if Cell(x, y) in list_cells:
                    return []
                while self.respects_forbidden_boundary(point, Cell(x, y)):
                    road.append(Cell(x, y))
                    if self.respects_forbidden_boundary(point, Cell(x + 1, y)):
                        break
                    y += 1
                    if y == self.__architecture.matrix_columns():
                        return []

        return road

    def down_and_left(self, point, cell, list_cells):
        """
        Buils a list of cells to the left until it is possible to move up
        or if it not possible to move to the left it moves down until it is possible to move left
        and then moves left until it is possible to move up
        :param point: the point
        :param cell: the current cell
        :param list_cells: the list of cells
        :return:the road of cells resulted

        """
        x = cell.get_x()
        y = cell.get_y()
        road = []
        if y >= 1 and self.respects_forbidden_boundary(point, Cell(x, y - 1)):
            road.append(Cell(x, y - 1))
            y -= 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x - 1, y)):
                    break
                y -= 1
                if y < 0:
                    return []
        elif x < self.__architecture.matrix_rows() - 1 and self.respects_forbidden_boundary(point, Cell(x + 1, y)):
            road.append(Cell(x + 1, y))
            x += 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x, y - 1)):
                    break
                x += 1
                if x == self.__architecture.matrix_rows():
                    return []
            if y >= 1 and self.respects_forbidden_boundary(point, Cell(x, y - 1)):
                road.append(Cell(x, y - 1))
                y -= 1
                if Cell(x, y) in list_cells:
                    return []
                while self.respects_forbidden_boundary(point, Cell(x, y)):
                    road.append(Cell(x, y))
                    if self.respects_forbidden_boundary(point, Cell(x - 1, y)):
                        break
                    y -= 1
                    if y < 0:
                        return []

        return road

    def down_and_right(self, point, cell, list_cells):
        """
        Buils a list of cells to the right until it is possible to move up
        or if it not possible to move to the right it moves down until it is possible to move right
        and then moves right until it is possible to move up
        :param point: the point
        :param cell: the current cell
        :param list_cells: the list of cells
        :return:the road of cells resulted

        """
        x = cell.get_x()
        y = cell.get_y()
        road = []
        if y < self.__architecture.matrix_columns() - 1 and self.respects_forbidden_boundary(point, Cell(x, y + 1)):
            road.append(Cell(x, y + 1))
            y += 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x - 1, y)):
                    break
                y += 1
                if y == self.__architecture.matrix_columns():
                    return []
        elif x < self.__architecture.matrix_rows() - 1 and self.respects_forbidden_boundary(point, Cell(x + 1, y)):
            road.append(Cell(x + 1, y))
            x += 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x, y + 1)):
                    break
                x += 1
                if x == self.__architecture.matrix_rows():
                    return []
            if y < self.__architecture.matrix_columns() - 1 and self.respects_forbidden_boundary(point,
                                                                                                 Cell(x, y + 1)):
                road.append(Cell(x, y + 1))
                y += 1
                if Cell(x, y) in list_cells:
                    return []
                while self.respects_forbidden_boundary(point, Cell(x, y)):
                    road.append(Cell(x, y))
                    if self.respects_forbidden_boundary(point, Cell(x - 1, y)):
                        break
                    y += 1
                    if y == self.__architecture.matrix_columns():
                        return []

        return road

    def road_through_two_branches_up(self, point, cell, cell_end, list_cells):
        """
        Function sees if is possible to find a road using two intermediate cells
        :param point:int
        :param cell:the current cell
        :param cell_end: the destination/ending cell
        :param list_cells:the list of cells
        :return:True/False if the road can be made
        """
        x = cell.get_x() - 1
        y = cell.get_y()
        end_y = cell_end.get_y()

        if not self.respects_forbidden_boundary(point, Cell(x, y)):
            return False

        while x >= 0:
            intermediateCell = Cell(x, end_y)
            if self.verifies_if_there_is_something_in_the_path_until_same_x(point, list_cells[-1], Cell(x, y)) \
                    and self.verifies_if_there_is_something_in_the_path_until_same_y(point, Cell(x, y),
                                                                                     intermediateCell) \
                    and self.verifies_if_there_is_something_in_the_path_until_same_x(point, intermediateCell, cell_end) \
                    and self.respects_forbidden_boundary(point, intermediateCell):
                if self.build_road_to_until_x(list_cells[-1], x, list_cells) and \
                        self.build_road_to_until_y(Cell(x, y), cell_end.get_y(), list_cells) \
                        and self.build_road_to_until_x(intermediateCell, cell_end.get_x(), list_cells):
                    return True

            x -= 1

        return False

    def road_through_two_branches_down(self, point, cell, cell_end, list_cells):
        """
        Function sees if is possible to find a road using two intermediate cells
        :param point:int
        :param cell:the current cell
        :param cell_end: the destination/ending cell
        :param list_cells:the list of cells
        :return:True/False if the road can be made
        """
        x = cell.get_x() + 1
        y = cell.get_y()
        end_y = cell_end.get_y()
        if not self.respects_forbidden_boundary(point, Cell(x, y)):
            return False
        while x < self.__architecture.matrix_rows():
            intermediateCell = Cell(x, end_y)
            if self.verifies_if_there_is_something_in_the_path_until_same_x(point, list_cells[-1], Cell(x, y)) \
                    and self.verifies_if_there_is_something_in_the_path_until_same_y(point, Cell(x, y),
                                                                                     intermediateCell) \
                    and self.verifies_if_there_is_something_in_the_path_until_same_x(point, intermediateCell, cell_end) \
                    and self.respects_forbidden_boundary(point, intermediateCell):
                if self.build_road_to_until_x(list_cells[-1], x, list_cells) and \
                        self.build_road_to_until_y(Cell(x, y), cell_end.get_y(), list_cells) \
                        and self.build_road_to_until_x(intermediateCell, cell_end.get_x(), list_cells):
                    return True

            x += 1

        return False

    def road_through_two_branches_right(self, point, cell, cell_end, list_cells):
        """
        Function sees if is possible to find a road using two intermediate cells
        :param point:int
        :param cell:the current cell
        :param cell_end: the destination/ending cell
        :param list_cells:the list of cells
        :return:True/False if the road can be made
        """
        x = cell.get_x()
        y = cell.get_y() + 1
        end_x = cell_end.get_x()
        if Cell(x, y) in list_cells:
            return False
        while y < self.__architecture.matrix_columns():
            currentCell = Cell(x, y)
            if not self.respects_forbidden_boundary(point, currentCell):
                return False
            intermediateCell = Cell(end_x, y)

            if self.respects_forbidden_boundary(point, intermediateCell) and \
                    self.verifies_if_there_is_something_in_the_path_until_same_x(point, currentCell,
                                                                                 intermediateCell) and \
                    self.verifies_if_there_is_something_in_the_path_until_same_y(point, intermediateCell, cell_end):
                if self.build_road_to_until_y(list_cells[-1], currentCell.get_y(), list_cells) and \
                        self.build_road_to_until_x(currentCell, intermediateCell.get_x(), list_cells) and \
                        self.build_road_to_until_y(intermediateCell, cell_end.get_y(), list_cells):
                    return True

            y += 1
        return False

    def road_through_two_branches_left(self, point, cell, cell_end, list_cells):
        """
        Function sees if is possible to find a road using two intermediate cells
        :param point:int
        :param cell:the current cell
        :param cell_end: the destination/ending cell
        :param list_cells:the list of cells
        :return:True/False if the road can be made
        """
        x = cell.get_x()
        y = cell.get_y() - 1
        end_x = cell_end.get_x()
        if Cell(x, y) in list_cells:
            return False
        while y >= 0:
            currentCell = Cell(x, y)
            if not self.respects_forbidden_boundary(point, currentCell):
                return False
            intermediateCell = Cell(end_x, y)

            if self.respects_forbidden_boundary(point, intermediateCell) and \
                    self.verifies_if_there_is_something_in_the_path_until_same_x(point, currentCell,
                                                                                 intermediateCell) and \
                    self.verifies_if_there_is_something_in_the_path_until_same_y(point, intermediateCell, cell_end):
                if self.build_road_to_until_y(list_cells[-1], currentCell.get_y(), list_cells) and \
                        self.build_road_to_until_x(currentCell, intermediateCell.get_x(), list_cells) and \
                        self.build_road_to_until_y(intermediateCell, cell_end.get_y(), list_cells):
                    return True

            y -= 1
        return False

    def add_boundaries_list(self, point, list_cells):
        """
        Adds boundaries to the list of boundaries of the point
        :param point: the point
        :param list_cells:  list of cells that need to be added

        :return:
        """
        for cell in list_cells:
            x = cell.get_x()
            y = cell.get_y()
            self.__roads[point].add_cell(Cell(x, y))
            self.add_forbidden_boundary(point, Cell(x, y))

    def show_road_point(self):
        """
        Functia unde pornim constructia drumurilor
        :return:
        """
        list_condition = [1, 1]
        points_cells = self.__architecture.cell_points()
        for point in points_cells:
            if point != -1:
                if len(points_cells[point]) == 2:
                    try:
                        self.building_road(point, list_condition)
                    except Exception as ve:
                        print("There is no road or You introduced a number in another's one boundary ",
                              "The exception is : ", ve)
                        return
        for point in points_cells:
            if point != -1:
                if len(points_cells[point]) != 2:
                    try:
                        self.building_road_for_multiple(point)
                    except Exception as ve:
                        print("There is no road or You introduced a number in another's one boundary",
                              "The exception is : ", ve)
                        return

    def represent_roads(self):
        """
        Represents the roads made
        :return:
        """
        points_cells = self.__architecture.cell_points()
        for point in points_cells:
            if point != -1:
                roads = self.__roads_per_point[point]
                for road in roads:
                    list_road = road.get_road()
                    for cell in list_road:
                        self.__architecture.set_x_y(cell.get_x(), cell.get_y(), point)

    def if_road_does_not_respect_boundaries_for_step_3(self):
        """
        Function finds the Cells that do not respect the boundaries of other points
        :return: list of cells that do not respect boundaries
        """
        cell_points = self.__architecture.cell_points()
        list_cells_to_colour_weird = []
        for point in cell_points:
            for point_2 in cell_points:
                if point != point_2:
                    cell_points_1 = cell_points[point]
                    for cell in cell_points_1:
                        x = cell.get_x()
                        y = cell.get_y()
                        if (Cell(x + 1, y) in cell_points[point_2] and Cell(x - 1, y) in cell_points[point_2]) or \
                                (Cell(x, y + 1) in cell_points[point_2] and Cell(x, y - 1) in cell_points[point_2]):
                            cell_points[point].remove(cell)
                            list_cells_to_colour_weird.append(cell)

        return list_cells_to_colour_weird

    def max_point(self):
        """
        Function finds the maximum point
        :return: the maximum point value
        """
        max_p = 0

        cell_points = self.__architecture.cell_points()

        for point in cell_points:
            if point > max_p:
                max_p = point

        return max_p

    def represent_points(self):
        """
        Function represents Cells that don't respect boundaries by setting the matrix with the maximum point value+1
        so when it is represented in GUI it shows different
        :return:
        """
        cells_to_colour_weird = self.if_road_does_not_respect_boundaries_for_step_3()
        max_p = self.max_point()
        max_p += 1
        for cell in cells_to_colour_weird:
            self.__architecture.set_x_y(cell.get_x(), cell.get_y(), max_p)
            max_p += 1

    def road_1(self, point, cell, list_cells):
        """
        Buils a list of cells to the left until it is possible to move down
        or if it not possible to move to the left it moves down until it is possible to move left
        and then moves left until it is possible to move down
        :param point: the point
        :param cell: the current cell
        :param list_cells: the list of cells
        :return: the road of cells that can be made

        """
        x = cell.get_x()
        y = cell.get_y()
        road = []
        if y >= 1 and self.respects_forbidden_boundary(point, Cell(x, y - 1)):
            road.append(Cell(x, y - 1))
            y -= 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x + 1, y)):
                    break
                y -= 1
                if y < 0:
                    return []
        elif x < self.__architecture.matrix_rows() - 1 and self.respects_forbidden_boundary(point,
                                                                                            Cell(x + 1, y)):
            road.append(Cell(x + 1, y))
            x += 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x, y - 1)):
                    break
                x += 1
                if x == self.__architecture.matrix_rows():
                    return []
            if y >= 1 and self.respects_forbidden_boundary(point, Cell(x, y - 1)):
                road.append(Cell(x, y - 1))
                y -= 1
                if Cell(x, y) in list_cells:
                    return []
                while self.respects_forbidden_boundary(point, Cell(x, y)):
                    road.append(Cell(x, y))
                    if self.respects_forbidden_boundary(point, Cell(x + 1, y)):
                        break
                    y -= 1
                    if y < 0:
                        return []

        return road

    def road_2(self, point, cell, list_cells):
        """
        Buils a list of cells to the right until it is possible to move down
        or if it not possible to move to the right it moves down until it is possible to move right
        and then moves right until it is possible to move down
        :param point: the point
        :param cell: the current cell
        :param list_cells: the list of cells
        :return:

        """
        x = cell.get_x()
        y = cell.get_y()
        road = []
        if y < self.__architecture.matrix_columns() - 1 and self.respects_forbidden_boundary(point, Cell(x, y + 1)):
            road.append(Cell(x, y + 1))
            y += 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x + 1, y)):
                    break
                y += 1
                if y == self.__architecture.matrix_columns():
                    return []
        elif x < self.__architecture.matrix_rows() - 1 and self.respects_forbidden_boundary(point, Cell(x + 1, y)):
            road.append(Cell(x + 1, y))
            x += 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x, y + 1)):
                    break
                x += 1
                if x == self.__architecture.matrix_rows():
                    return []
            if y < self.__architecture.matrix_columns() - 1 and self.respects_forbidden_boundary(point,
                                                                                                 Cell(x, y + 1)):
                road.append(Cell(x, y + 1))
                y += 1
                if Cell(x, y) in list_cells:
                    return []
                while self.respects_forbidden_boundary(point, Cell(x, y)):
                    road.append(Cell(x, y))
                    if self.respects_forbidden_boundary(point, Cell(x + 1, y)):
                        break
                    y += 1
                    if y == self.__architecture.matrix_columns():
                        return []

        return road

    def road_3(self, point, cell, list_cells):
        """
        Buils a list of cells to the left until it is possible to move up
        or if it not possible to move to the left it moves up until it is possible to move left
        and then moves left until it is possible to move up
        :param point: the point
        :param cell: the current cell
        :param list_cells: the list of cells
        :return:

        """

        x = cell.get_x()
        y = cell.get_y()
        road = []
        if y >= 1 and self.respects_forbidden_boundary(point, Cell(x, y - 1)):
            road.append(Cell(x, y - 1))
            y -= 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x - 1, y)):
                    break
                y -= 1
                if y < 0:
                    return []
        elif x >= 1 and self.respects_forbidden_boundary(point, Cell(x - 1, y)):
            road.append(Cell(x - 1, y))
            x -= 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x, y - 1)):
                    break
                x -= 1
                if x < 0:
                    return []

            if y >= 1 and self.respects_forbidden_boundary(point, Cell(x, y - 1)):
                road.append(Cell(x, y - 1))
                y -= 1
                if Cell(x, y) in list_cells:
                    return []
                while self.respects_forbidden_boundary(point, Cell(x, y)):
                    road.append(Cell(x, y))
                    if self.respects_forbidden_boundary(point, Cell(x - 1, y)):
                        break
                    y -= 1
                    if y < 0:
                        return []

        return road

    def road_4(self, point, cell, list_cells):
        """
        Buils a list of cells to the right until it is possible to move up
        or if it not possible to move to the right it moves up until it is possible to move right
        and then moves right until it is possible to move up
        :param point: the point
        :param cell: the current cell
        :param list_cells: the list of cells
        :return:

        """
        x = cell.get_x()
        y = cell.get_y()
        road = []
        if y < self.__architecture.matrix_columns() - 1 and self.respects_forbidden_boundary(point, Cell(x, y + 1)):
            road.append(Cell(x, y + 1))
            y += 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x - 1, y)):
                    break
                y += 1
                if y == self.__architecture.matrix_columns():
                    return []
        elif x >= 1 and self.respects_forbidden_boundary(point, Cell(x - 1, y)):
            road.append(Cell(x - 1, y))
            x -= 1
            if Cell(x, y) in list_cells:
                return []
            while self.respects_forbidden_boundary(point, Cell(x, y)):
                road.append(Cell(x, y))
                if self.respects_forbidden_boundary(point, Cell(x, y - 1)):
                    break
                x -= 1
                if x < 0:
                    return []

            if y < self.__architecture.matrix_columns() - 1 and self.respects_forbidden_boundary(point, Cell(x, y + 1)):
                road.append(Cell(x, y + 1))
                y += 1
                if Cell(x, y) in list_cells:
                    return []
                while self.respects_forbidden_boundary(point, Cell(x, y)):
                    road.append(Cell(x, y))
                    if self.respects_forbidden_boundary(point, Cell(x - 1, y)):
                        break
                    y += 1
                    if y == self.__architecture.matrix_columns():
                        return []

        return road
