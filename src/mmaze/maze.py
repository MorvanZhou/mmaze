import typing as tp
import random

import mmaze
from mmaze import visual


class Maze:
    def __init__(self, width, height, value: int = 1):
        self._base_width = width
        self._base_height = height
        self._width = width * 2 + 1
        self._height = height * 2 + 1
        self.data: tp.List[tp.List[int]] = [[value] * self._width for _ in range(self._height)]

    def find_neighbors(self, r: int, c: int, is_wall: bool = False) -> tp.List[tp.Tuple[int, int]]:
        """Find all the grid neighbors of the current position; visited, or not.

        Args:
            r (int): row of cell of interest
            c (int): column of cell of interest
            is_wall (bool): Are we looking for neighbors that are walls, or open cells?
        Returns:
            list: all neighboring cells that match our request
        """

        ns = []

        if r > 1 and self.data[r - 2][c] == is_wall:
            ns.append((r - 2, c))
        if r < self.height - 2 and self.data[r + 2][c] == is_wall:
            ns.append((r + 2, c))
        if c > 1 and self.data[r][c - 2] == is_wall:
            ns.append((r, c - 2))
        if c < self.width - 2 and self.data[r][c + 2] == is_wall:
            ns.append((r, c + 2))

        random.shuffle(ns)
        return ns

    def random_position(self):
        return random.randrange(1, self._height, 2), random.randrange(1, self._width, 2)

    def set(self, row: int, col: int, value):
        self.data[row][col] = value

    def get(self, row: int, col: int) -> int:
        return self.data[row][col]

    def plot(self, solution=None):
        visual.plot(self, solution)

    def save(self, path: str, solution=None):
        visual.save(path, self, solution)

    def solve(self, start: tp.Sequence[int], end: tp.Sequence[int], method: str = "backtracking") -> tp.Sequence:
        return mmaze.solve(self, start, end, method)

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def base_height(self):
        return self._base_height

    @property
    def base_width(self):
        return self._base_width

    def tostring(self):
        if self.data is None:
            return ""

        # build the walls of the grid
        txt = []
        for row in self.data:
            txt.append("".join(["#" if cell else " " for cell in row]))

        return "\n".join(txt)

    def __str__(self):
        """display maze walls, entrances, and solutions, if available

        Returns:
            str: string representation of the maze
        """
        return self.tostring()

    def __repr__(self):
        """display maze walls, entrances, and solutions, if available

        Returns:
            str: string representation of the maze
        """
        return self.__str__()
