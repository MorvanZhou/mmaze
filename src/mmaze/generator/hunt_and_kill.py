import random

from mmaze.generator.base import BaseMazeGenerator
from mmaze.maze import Maze

RANDOM = 1
SERPENTINE = 2


class HuntAndKill(BaseMazeGenerator):
    """
    1. Randomly choose a starting cell.
    2. Perform a random walk from the current cel, carving passages to unvisited neighbors,
        until the current cell has no unvisited neighbors.
    3. Select a new grid cell; if it has been visited, walk from it.
    4. Repeat steps 2 and 3 a sufficient number of times that there the probability of a cell
        not being visited is extremely small.

    In this implementation of Hunt-and-kill there are two different ways to select a new grid cell in step 2.  The first
    is serpentine through the grid (the classic solution), the second is to randomly select a new cell enough times that
    the probability of an unexplored cell is very, very low. The second option includes a small amount of risk, but it
    creates a more interesting, harder maze.
    """

    def __init__(self, hunt_order="random"):
        super().__init__()

        # the user can define what order to hunt for the next cell in
        if hunt_order.lower().strip() == "serpentine":
            self.ho = SERPENTINE
        else:
            self.ho = RANDOM

    def generate(self, width: int, height: int) -> Maze:
        m = Maze(width, height, value=1)
        # find an arbitrary starting position
        row, col = m.random_position()
        m.set(row, col, 0)

        # perform many random walks, to fill the maze
        num_trials = 0
        while (row, col) != (-1, -1):
            self._walk(m, row, col)
            row, col = self._hunt(m, num_trials)
            num_trials += 1

        return m

    @staticmethod
    def _walk(maze: Maze, row, col):
        """This is a standard random walk. It must start from a visited cell.
        And it completes when the current cell has no unvisited neighbors.

        Args:
            row (int): row index
            col (int): col index
        Returns: None
        """
        if maze.get(row, col) == 0:
            this_row = row
            this_col = col
            unvisited_neighbors = maze.find_neighbors(this_row, this_col, True)

            while len(unvisited_neighbors) > 0:
                neighbor = random.choice(unvisited_neighbors)
                maze.set(neighbor[0], neighbor[1], 0)
                maze.set((neighbor[0] + this_row) // 2, (neighbor[1] + this_col) // 2, 0)
                this_row, this_col = neighbor
                unvisited_neighbors = maze.find_neighbors(this_row, this_col, True)

    def _hunt(self, maze: Maze, count):
        """Based on how this algorithm was configured, choose hunt for the next starting point.

        Args:
            count (int): how long to iterate
        Returns:
            tuple: position of next cell
        """
        if self.ho == SERPENTINE:
            return self._hunt_serpentine(maze, count)
        else:
            return self._hunt_random(maze.width, maze.height, count)

    @staticmethod
    def _hunt_random(width, height, count):
        """Select the next cell to walk from, randomly.

        Args:
            count (int): row index
        Returns:
            tuple: position of next cell
        """
        if count >= (height * width):
            return -1, -1

        return random.randrange(1, height, 2), random.randrange(1, width, 2)

    @staticmethod
    def _hunt_serpentine(maze: Maze, count):
        """Select the next cell to walk from by cycling through every grid cell in order.

        Args:
            count (int): how long to iterate
        Returns:
            tuple: position of next cell
        """
        row, col = (1, 1)
        found = False

        while not found:
            col = col + 2
            if col > (maze.width - 2):
                row += 2
                col = 1
                if row > (maze.height - 2):
                    return -1, -1

            if (
                maze.set(row, col, 0)
                and len(maze.find_neighbors(row, col, True)) > 0
            ):
                found = True

        return row, col
