from abc import ABCMeta, abstractmethod
import typing as tp
import random

from mmaze.maze import Maze


class BaseSolver(metaclass=ABCMeta):
    def __init__(self, prune=True):
        self.grid = None
        self.start = None
        self.end = None
        self.prune = prune

    def solve(self, maze: Maze, start: tp.Sequence[int], end: tp.Sequence[int]):
        """helper method to solve a init the solver before solving the maze

        Args:
            maze (Maze): maze
            start (tuple): position in maze to start from
            end (tuple): position in maze to finish at
        Returns:
            list: final solutions
        """
        self.grid = maze.data
        self.start = tuple([s * 2 + 1 for s in start])
        self.end = tuple([e * 2 + 1 for e in end])
        self._pre_check(start, end)
        solutions = self._solve()
        if self.prune:
            solutions = self.prune_solutions(solutions)
        return solutions

    def _pre_check(self, start, end):
        """ensure the maze mazes any sense before you solve it

        Args:
            start: position in maze to start from
            end: position in maze to finish at
        Returns: None
        """

        # validating checks
        assert 0 <= start[0] < len(self.grid), "Entrance is outside the grid."
        assert 0 <= start[1] < len(self.grid[0]), "Entrance is outside the grid."
        assert 0 <= end[0] < len(self.grid), "Entrance is outside the grid."
        assert 0 <= end[1] < len(self.grid[0]), "Entrance is outside the grid."

    @abstractmethod
    def _solve(self):
        ...

    """
    All of the methods below this are helper methods,
    common to many maze-solving algorithms.
    """

    def _find_unblocked_neighbors(self, pos):
        """Find all the grid neighbors of the current position; visited, or not.

        Args:
            pos (tuple): cell of interest
        Returns:
            list: all the unblocked neighbors to this cell
        """
        r, c = pos
        ns = []

        if r > 1 and not self.grid[r - 1][c] and not self.grid[r - 2][c]:
            ns.append((r - 2, c))
        if (
            r < len(self.grid) - 2
            and not self.grid[r + 1][c]
            and not self.grid[r + 2][c]
        ):
            ns.append((r + 2, c))
        if c > 1 and not self.grid[r][c - 1] and not self.grid[r][c - 2]:
            ns.append((r, c - 2))
        if (
            c < len(self.grid[0]) - 2
            and not self.grid[r][c + 1]
            and not self.grid[r][c + 2]
        ):
            ns.append((r, c + 2))

        random.shuffle(ns)
        return ns

    def _midpoint(self, a, b):
        """Find the wall cell between to passage cells

        Args:
            a (tuple): first cell
            b (tuple): second cell
        Returns:
            tuple: cell half way between the first two
        """
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2

    def _move(self, start, direction):
        """Convolve a position tuple with a direction tuple to generate a new position.

        Args:
            start (tuple): position cell to start at
            direction (tuple): vector cell of direction to travel to
        Returns:
            tuple: end result of movement
        """
        return tuple(map(sum, zip(start, direction)))

    def _on_edge(self, cell: tp.Sequence[int]):
        """Does the cell lay on the edge, rather inside of the maze grid?

        Args:
            cell: some place in the grid
        Returns:
            bool: Is the cell on the edge of the maze?
        """
        r, c = cell

        if r == 0 or r == len(self.grid) - 1:
            return True
        if c == 0 or c == len(self.grid[0]) - 1:
            return True

        return False

    def _push_edge(self, cell: tp.Sequence[int]):
        """You may need to find the cell directly inside of a start or end cell.

        Args:
            cell: some place in the grid
        Returns:
            tuple: the new cell location, pushed from the edge
        """
        r, c = cell

        if r == 0:
            return 1, c
        elif r == (len(self.grid) - 1):
            return r - 1, c
        elif c == 0:
            return r, 1
        else:
            return r, c - 1

    def _within_one(self, cell: tp.Sequence[int], desire: tp.Sequence[int]):
        """Is the current cell within one move of the desired cell?
        Note, this might be one full more, or one half move.

        Args:
            cell: position to start at
            desire: position you want to be at
        Returns:
            bool: Are you within one movement of your goal?
        """
        if not cell or not desire:
            return False

        if cell[0] == desire[0]:
            if abs(cell[1] - desire[1]) < 2:
                return True
        elif cell[1] == desire[1]:
            if abs(cell[0] - desire[0]) < 2:
                return True

        return False

    def _prune_solution(self, solution):
        """In the process of solving a maze, the algorithm might go down
        the wrong corridor then backtrack. These extraneous steps need to be removed.
        Also, clean up the end points.

        Args:
            solution (list): raw maze solution
        Returns:
            list: cleaner, tightened up solution to the maze
        """
        found = True
        attempt = 0
        max_attempt = len(solution)

        while found and len(solution) > 2 and attempt < max_attempt:
            found = False
            attempt += 1

            for i in range(len(solution) - 1):
                first = solution[i]
                if first in solution[i + 1 :]:
                    first_i = i
                    last_i = solution[i + 1 :].index(first) + i + 1
                    found = True
                    break

            if found:
                solution = solution[:first_i] + solution[last_i:]

        # solution does not include entrances
        # if len(solution) > 1:
        #     if solution[0] == self.start:
        #         solution = solution[1:]
        #     if solution[-1] == self.end:
        #         solution = solution[:-1]

        return solution

    def prune_solutions(self, solutions):
        """prune all the duplicate cells from all solutions, and fix end points

        Args:
            solutions (list): multiple raw solutions
        Returns:
            list: the above solutions, cleaned up
        """
        return [self._prune_solution(s) for s in solutions]
