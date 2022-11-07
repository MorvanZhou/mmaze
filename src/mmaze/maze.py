import random
import typing as tp

import mmaze
from mmaze import visual
from mmaze.cell import CellType


class Maze:
    def __init__(self, width, height, cell_type: CellType = CellType.WALL):
        self._base_width = width
        self._base_height = height
        self._width = width * 2 + 1
        self._height = height * 2 + 1
        self.data: tp.List[tp.List[CellType]] = [[cell_type] * self._width for _ in range(self._height)]
        self.solutions = []

    def check_wall(self, row, col, is_wall):
        cell = self.get(row, col)
        if is_wall:
            return cell == CellType.WALL
        else:
            return cell != CellType.WALL

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

        if r > 1 and self.check_wall(r - 2, c, is_wall):
            ns.append((r - 2, c))
        if r < self.height - 2 and self.check_wall(r + 2, c, is_wall):
            ns.append((r + 2, c))
        if c > 1 and self.check_wall(r, c - 2, is_wall):
            ns.append((r, c - 2))
        if c < self.width - 2 and self.check_wall(r, c + 2, is_wall):
            ns.append((r, c + 2))

        random.shuffle(ns)
        return ns

    def random_position(self):
        return random.randrange(1, self._height, 2), random.randrange(1, self._width, 2)

    def set(self, row: int, col: int, cell_type: CellType):
        self.data[row][col] = cell_type

    def get(self, row: int, col: int) -> CellType:
        return self.data[row][col]

    def plot(
            self,
            start: tp.Optional[tp.Sequence[int]] = None,
            end: tp.Optional[tp.Sequence[int]] = None,
            solution: tp.Optional[tp.Sequence[tp.Sequence]] = None
    ):
        visual.plot(self, start, end, solution)

    def save(
            self,
            path: str,
            start: tp.Optional[tp.Sequence[int]] = None,
            end: tp.Optional[tp.Sequence[int]] = None,
            solution: tp.Optional[tp.Sequence[tp.Sequence]] = None
    ):
        visual.save(path, self, start, end, solution)

    def solve(
            self,
            start: tp.Sequence[int],
            end: tp.Sequence[int],
            method: str = "backtracking"
    ) -> tp.Sequence:
        self.solutions = mmaze.solve(self, start, end, method)
        return self.solutions

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

    def to_number(
            self,
            start: tp.Optional[tp.Sequence[int]] = None,
            end: tp.Optional[tp.Sequence[int]] = None,
            solution: tp.Optional[tp.Sequence[tp.Sequence]] = None,
    ) -> tp.List[tp.List[int]]:
        if self.data is None:
            return []
        res = []
        for row in self.data:
            res_row = []
            for cell in row:
                res_row.append(cell.value)
            res.append(res_row)
        if start is not None:
            p = [p * 2 + 1 for p in start]
            res[p[0]][p[1]] = CellType.START.value
        if end is not None:
            p = [p * 2 + 1 for p in end]
            res[p[0]][p[1]] = CellType.END.value
        if solution is not None:
            for i, p in enumerate(solution):
                res[p[0]][p[1]] = CellType.SOLUTION.value
        return res

    def tostring(
            self,
            start: tp.Optional[tp.Sequence[int]] = None,
            end: tp.Optional[tp.Sequence[int]] = None,
            solution: tp.Optional[tp.Sequence[tp.Sequence]] = None,
    ):
        if self.data is None:
            return ""

        # build the walls of the grid
        txt = []
        for row in self.data:
            str_row = []
            for cell in row:
                if cell == CellType.WALL:
                    str_row.append("■")
                elif cell == CellType.ROAD:
                    str_row.append(" ")
            txt.append(str_row)

        if solution is not None:
            for i, p in enumerate(solution):
                txt[p[0]][p[1]] = "*"

        if start is not None:
            p = [p * 2 + 1 for p in start]
            txt[p[0]][p[1]] = "S"
        if end is not None:
            p = [p * 2 + 1 for p in end]
            txt[p[0]][p[1]] = "E"
        return "\n".join("".join(row) for row in txt)

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
