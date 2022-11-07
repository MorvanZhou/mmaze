import random

from mmaze.generator.base import BaseMazeGenerator, set_cell
from mmaze.maze import Maze
from mmaze.cell import CellType


class GrowingTree(BaseMazeGenerator):
    """
    1. Let C be a list of cells, initially empty. Add one cell to C, at random.
    2. Choose a cell from C, and carve a passage to any unvisited neighbor of that cell,
        adding that neighbor to C as well. If there are no unvisited neighbors,
        remove the cell from C.
    3. Repeat step 2 until C is empty.

    Optional Parameters

    backtrack_chance: float [0.0, 1.0]
        Splits the logic to either use Recursive Backtracking (RB) or Prim's (random)
        to select the next cell to visit. (default 1.0)
    """
    symmetry_ok = True

    def __init__(self, backtrack_chance=1.0):
        super().__init__()
        self.backtrack_chance = backtrack_chance

    def _generate(self, width: int, height: int, symmetry: str = "none") -> Maze:
        m = Maze(width, height, CellType.WALL)
        row, col = m.random_position()
        active = []
        set_cell(m, (row, col), CellType.ROAD, symmetry, active)

        # continue until you have no more neighbors to move to
        while active:
            if random.random() < self.backtrack_chance:
                row, col = active[-1]
            else:
                row, col = random.choice(active)

            # find a visited neighbor
            next_neighbors = m.find_neighbors(row, col, is_wall=True)
            if len(next_neighbors) == 0:
                active = [a for a in active if a != (row, col)]
                continue

            row_, col_ = random.choice(next_neighbors)
            set_cell(m, (row_, col_), CellType.ROAD, symmetry, active)
            set_cell(m, ((row + row_) // 2, (col + col_) // 2), CellType.ROAD, symmetry)

        return m
