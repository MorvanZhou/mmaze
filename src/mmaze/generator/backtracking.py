from mmaze.generator.base import BaseMazeGenerator, set_cell
from mmaze.maze import Maze
from mmaze.cell import CellType


class Backtracking(BaseMazeGenerator):
    """
    1. Randomly choose a starting cell.
    2. Randomly choose a wall at the current cell and open a passage through to any random adjacent
        cell, that has not been visited yet. This is now the current cell.
    3. If all adjacent cells have been visited, back up to the previous and repeat step 2.
    4. Stop when the algorithm has backed all the way up to the starting cell.
    """
    symmetry_ok = True

    def _generate(self, width: int, height: int, symmetry: str = "none") -> Maze:
        m = Maze(width, height, cell_type=CellType.WALL)

        row, col = m.random_position()
        track = []
        set_cell(m, (row, col), CellType.ROAD, symmetry, track)

        while track:
            (row, col) = track[-1]
            neighbors = m.find_neighbors(row, col, is_wall=True)

            if len(neighbors) == 0:
                track = track[:-1]
            else:
                row_, col_ = neighbors[0]
                set_cell(m, (row_, col_), CellType.ROAD, symmetry, track)
                set_cell(m, ((row_ + row) // 2, (col_ + col) // 2), CellType.ROAD, symmetry)

        return m
