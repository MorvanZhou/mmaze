import random

from mmaze.generator.base import BaseMazeGenerator
from mmaze.maze import Maze


class BinaryTree(BaseMazeGenerator):
    """For every cell in the grid, knock down a wall either North or West."""

    def __init__(self, skew=None):
        super().__init__()
        skewes = {
            "NW": [(1, 0), (0, -1)],
            "NE": [(1, 0), (0, 1)],
            "SW": [(-1, 0), (0, -1)],
            "SE": [(-1, 0), (0, 1)],
        }
        if skew in skewes:
            self.skew = skewes[skew]
        else:
            key = random.choice(list(skewes.keys()))
            self.skew = skewes[key]

    def generate(self, width: int, height: int) -> Maze:
        m = Maze(width, height, 1)

        for row in range(1, m.height, 2):
            for col in range(1, m.width, 2):
                m.set(row, col, 0)
                neighbor_row, neighbor_col = self._find_neighbor(m.width, m.height, row, col)
                m.set(neighbor_row, neighbor_col, 0)

        return m

    def _find_neighbor(self, maze_width: int, maze_height: int, row: int, col: int):
        """Find a neighbor in the skewed direction.

        Args:
            row (int): row number
            col (int): col number
        Returns:
            tuple: position of the randomly-chosen neighbor
        """
        neighbors = []
        for b_row, b_col in self.skew:
            neighbor_row = row + b_row
            neighbor_col = col + b_col
            if 0 < neighbor_row < (maze_height - 1):
                if 0 < neighbor_col < (maze_width - 1):
                    neighbors.append((neighbor_row, neighbor_col))

        if len(neighbors) == 0:
            return row, col
        else:
            return random.choice(neighbors)
