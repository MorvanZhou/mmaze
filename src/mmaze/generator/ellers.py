import random
import typing as tp

from mmaze.generator.base import BaseMazeGenerator
from mmaze.maze import Maze
from mmaze.cell import CellType


class Ellers(BaseMazeGenerator):
    """
    1. Put the cells of the first row each in their own set.
    2. Join adjacent cells. But not if they are already in the same set.
        Merge the sets of these cells.
    3. For each set in the row, create at least one vertical connection down to the next row.
    4. Put any unconnected cells in the next row into their own set.
    5. Repeast until the last row.
    6. In the last row, join all adjacent cells that do not share a set.
    """
    symmetry_ok = False

    def __init__(self, xskew=0.5, yskew=0.5):
        super().__init__()
        self.xskew = 0.0 if xskew < 0.0 else 1.0 if xskew > 1.0 else xskew
        self.yskew = 0.0 if yskew < 0.0 else 1.0 if yskew > 1.0 else yskew

    def _generate(self, width: int, height: int, **kwargs) -> Maze:
        m = Maze(width, height, CellType.ROAD)
        # create empty grid, with walls
        sets = [[-1] * m.width for _ in range(m.height)]

        # initialize the first row cells to each exist in their own set
        max_set_number = 0

        # process all but the last row
        for r in range(1, m.height - 1, 2):
            max_set_number = self._init_row(sets, r, max_set_number, m.width)
            self._merge_one_row(sets, r, m.width, m.height)
            self._merge_down_a_row(sets, r, m.width, m.height)

        # process last row
        _ = self._init_row(sets, m.height - 2, max_set_number, m.width)
        self._process_last_row(sets, m.width, m.height)

        # translate grid cell sets into a maze
        self._set_grid_from_sets(sets, m)
        return m

    @staticmethod
    def _init_row(sets, row, max_set_number, width):
        """Initialize each cell in a row to its own set

        Args:
            sets (list): grid representation of row sets
            row (int): row number
            max_set_number (int): counter used to determine how many rows/sets are left to work on
        Returns:
            int: latest counter for number of sets left to work on
        """
        for c in range(1, width, 2):
            if sets[row][c] < 0:
                sets[row][c] = max_set_number
                max_set_number += 1

        return max_set_number

    def _merge_one_row(self, sets: tp.List[tp.List[int]], r, width, height):
        """randomly decide to merge cells within a column

        Args:
            sets (list): grid representation of row sets
            r (int): row number
        Returns: None
        """
        for c in range(1, width - 2, 2):
            if random.random() < self.xskew:
                if sets[r][c] != sets[r][c + 2]:
                    sets[r][c + 1] = sets[r][c]
                    self._merge_sets(sets, sets[r][c + 2], sets[r][c], width, height, max_row=r)

    def _merge_down_a_row(self, sets, start_row, width, height):
        """Create vertical connections in the maze.
        For the current row, cut down at least one passage for each cell set.

        Args:
            sets (list): grid representation of row sets
            start_row (int): index of row to start merging from
        Returns: None
        """
        # this is not meant for the bottom row
        if start_row == height - 2:
            return

        # count how many cells of each set exist in a row
        set_counts = {}
        for c in range(1, width, 2):
            s = sets[start_row][c]
            if s not in set_counts:
                set_counts[s] = [c]
            else:
                set_counts[s] = set_counts[s] + [c]

        # merge down randomly, but at least once per set
        for s in set_counts:
            c = random.choice(set_counts[s])
            sets[start_row + 1][c] = s
            sets[start_row + 2][c] = s

        for c in range(1, width - 2, 2):
            if random.random() < self.yskew:
                s = sets[start_row][c]
                if sets[start_row + 1][c] == -1:
                    sets[start_row + 1][c] = s
                    sets[start_row + 2][c] = s

    @staticmethod
    def _merge_sets(sets, from_set, to_set, width, height, max_row=-1):
        """merge two different sets of grid cells into one
        To improve performance, the grid will only be searched up to some maximum row number.

        Args:
            sets (list): grid representation of row sets
            from_set (int): set to merge FROM
            to_set (int): set to merge TO
            max_row (int): index of last row in the maze
        Returns: None
        """
        if max_row < 0:
            max_row = height - 1

        for r in range(1, max_row + 1):
            for c in range(1, width - 1):
                if sets[r][c] == from_set:
                    sets[r][c] = to_set

    def _process_last_row(self, sets, width, height):
        """join all adjacent cells that do not share a set, and omit the vertical connections

        Args:
            sets (list): grid representation of row sets
        Returns: None
        """
        r = height - 2
        for c in range(1, width - 2, 2):
            if sets[r][c] != sets[r][c + 2]:
                sets[r][c + 1] = sets[r][c]
                self._merge_sets(sets, sets[r][c + 2], sets[r][c], width, height)

    @staticmethod
    def _set_grid_from_sets(sets, maze: Maze) -> None:
        """translate the maze sets into a maze grid

        Args:
            sets (list): grid representation of row sets
        """

        for r in range(maze.height):
            for c in range(maze.width):
                if sets[r][c] == -1:
                    maze.set(r, c, CellType.WALL)
