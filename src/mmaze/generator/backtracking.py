from mmaze.generator.base import BaseMazeGenerator
from mmaze.maze import Maze


class Backtracking(BaseMazeGenerator):
    """
    1. Randomly choose a starting cell.
    2. Randomly choose a wall at the current cell and open a passage through to any random adjacent
        cell, that has not been visited yet. This is now the current cell.
    3. If all adjacent cells have been visited, back up to the previous and repeat step 2.
    4. Stop when the algorithm has backed all the way up to the starting cell.
    """

    def __init__(self):
        super().__init__()  # create empty grid, with walls

    def generate(self, width: int, height: int) -> Maze:
        m = Maze(width, height, value=1)

        row, col = m.random_position()
        track = [(row, col)]
        m.set(row, col, 0)

        while track:
            (row, col) = track[-1]
            neighbors = m.find_neighbors(row, col, is_wall=True)

            if len(neighbors) == 0:
                track = track[:-1]
            else:
                row_, col_ = neighbors[0]
                m.set(row_, col_, 0)
                m.set((row_ + row) // 2, (col_ + col) // 2, 0)

                track += [(row_, col_)]

        return m
