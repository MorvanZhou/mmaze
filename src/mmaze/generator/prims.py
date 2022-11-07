import random

from mmaze.generator.base import BaseMazeGenerator, set_cell
from mmaze.maze import Maze
from mmaze.cell import CellType


class Prims(BaseMazeGenerator):
    """
    The Algorithm

    1. Choose an arbitrary cell from the grid, and add it to some
        (initially empty) set visited nodes (V).
    2. Randomly select a wall from the grid that connects a cell in
        V with another cell not in V.
    3. Add that wall to the Minimal Spanning Tree (MST), and the edge's other cell to V.
    4. Repeat steps 2 and 3 until V includes every cell in G.
    """
    symmetry_ok = True

    def _generate(self, width: int, height: int, symmetry: str = "none") -> Maze:
        m = Maze(width, height, CellType.WALL)
        # choose a random starting position
        row, col = m.random_position()
        set_cell(m, (row, col), CellType.ROAD, symmetry)

        # created a weighted list of all vertices connected in the graph
        neighbors = m.find_neighbors(row, col, True)

        while len(neighbors) >= 1:
            # find neighbor with lowest weight, make it current
            nn = random.randrange(len(neighbors))
            row, col = neighbors[nn]
            set_cell(m, (row, col), CellType.ROAD, symmetry)

            neighbors = neighbors[:nn] + neighbors[nn + 1:]
            # connect that neighbor to a random neighbor with grid[posi] == 0
            nearest_n0, nearest_n1 = m.find_neighbors(row, col)[0]
            set_cell(m, ((row + nearest_n0) // 2, (col + nearest_n1) // 2), CellType.ROAD, symmetry)

            # find all unvisited neighbors of current, add them to neighbors
            unvisited = m.find_neighbors(row, col, True)
            neighbors = list(set(neighbors + unvisited))

        return m
