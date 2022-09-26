import random

from mmaze.generator.base import BaseMazeGenerator
from mmaze.maze import Maze


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

    def __init__(self):
        super().__init__()

    def generate(self, width: int, height: int) -> Maze:
        m = Maze(width, height, 1)
        # choose a random starting position
        row, col = m.random_position()
        m.set(row, col, 0)

        # created a weighted list of all vertices connected in the graph
        neighbors = m.find_neighbors(row, col, True)

        # loop over all current neighbors, until empty
        visited = 1

        while visited < m.base_height * m.base_width:
            # find neighbor with lowest weight, make it current
            nn = random.randrange(len(neighbors))
            row, col = neighbors[nn]
            visited += 1
            m.set(row, col, 0)
            neighbors = neighbors[:nn] + neighbors[nn + 1:]
            # connect that neighbor to a random neighbor with grid[posi] == 0
            nearest_n0, nearest_n1 = m.find_neighbors(row, col)[0]
            m.set((row + nearest_n0) // 2, (col + nearest_n1) // 2, 0)

            # find all unvisited neighbors of current, add them to neighbors
            unvisited = m.find_neighbors(row, col, True)
            neighbors = list(set(neighbors + unvisited))

        return m
