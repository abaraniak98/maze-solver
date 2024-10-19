from tkinter import Tk, BOTH, Canvas

from window import Window
from maze import *

def main():
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    seed = random.seed(0)
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, seed, win)

    maze.solve()

    win.wait_for_close()

if __name__ == "__main__":
    main()