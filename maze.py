from tkinter import Tk, BOTH, Canvas
import time
import random


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line():
    def __init__(self, start_point, end_point):
        self.__start_point = start_point
        self.__end_point = end_point

    def draw(self, canvas, fill_color="black"):
        x1 = self.__start_point.x
        y1 = self.__start_point.y
        x2 = self.__end_point.x
        y2 = self.__end_point.y
        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)


class Cell():
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)))
        else:
            self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "white")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)))
        else:
            self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "white")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)))
        else:
            self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "white")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)))
        else:
            self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "white")

    def draw_move(self, dest_cell, undo=False):
        start_cell_center_x = abs(self._x2 - self._x1) // 2 + self._x1
        start_cell_center_y = abs(self._y2 - self._y1) // 2 + self._y1
        dest_cell_center_x = abs(dest_cell._x2 - dest_cell._x1) // 2 + dest_cell._x1
        dest_cell_center_y = abs(dest_cell._y2 - dest_cell._y1) // 2 + dest_cell._y1
        start_cell_center = Point(start_cell_center_x, start_cell_center_y)
        dest_cell_center = Point(dest_cell_center_x, dest_cell_center_y)
        color = "red"
        if undo:
            color = "gray"
        self._win.draw_line(Line(start_cell_center, dest_cell_center), color)


class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        seed=None,
        win=None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._seed = seed
        self._win = win

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()
        
    def _create_cells(self):
        print(self._num_cols)
        print(self._num_rows)
        self._cells = [[Cell(self._win) for _ in range(self._num_rows)] for _ in range(self._num_cols)]
        print(len(self._cells))
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        cell_x1 = self._x1 + i * self._cell_size_x
        cell_y1 = self._y1 + j * self._cell_size_y
        cell_x2 = cell_x1 + self._cell_size_x
        cell_y2 = cell_y1 + self._cell_size_y
        self._cells[i][j].draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.02)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1,self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            to_be_visited = []

            if i > 0 and not self._cells[i-1][j].visited:
                to_be_visited.append((i-1, j))
            if j > 0 and not self._cells[i][j-1].visited:
                to_be_visited.append((i, j-1))
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited:
                to_be_visited.append((i+1, j))
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited:
                to_be_visited.append((i, j+1))

            if len(to_be_visited) == 0:
                self._draw_cell(i, j)
                return

            direction_index = random.randrange(len(to_be_visited))
            direction = to_be_visited[direction_index]

            if direction[0] == i+1:
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False
            if direction[0] == i-1:
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False
            if direction[1] == j+1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False
            if direction[1] == j-1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False

            self._break_walls_r(direction[0], direction[1])
        
    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0,0)
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if self._cells[i][j] == self._cells[self._num_cols - 1][self._num_rows - 1]:
            return True
        
        to_be_visited = []

        if i > 0 and not self._cells[i-1][j].visited and not self._cells[i][j].has_left_wall:
            to_be_visited.append((i-1, j))
        if j > 0 and not self._cells[i][j-1].visited and not self._cells[i][j].has_top_wall:
            to_be_visited.append((i, j-1))
        if i < self._num_cols - 1 and not self._cells[i+1][j].visited and not self._cells[i][j].has_right_wall:
            to_be_visited.append((i+1, j))
        if j < self._num_rows - 1 and not self._cells[i][j+1].visited and not self._cells[i][j].has_bottom_wall:
            to_be_visited.append((i, j+1))
        
        for cell in to_be_visited:
            self._cells[i][j].draw_move(self._cells[cell[0]][cell[1]])
            if self._solve_r(cell[0], cell[1]) == True:
                return True
            self._cells[i][j].draw_move(self._cells[cell[0]][cell[1]], undo = True)

        return False
   
          
