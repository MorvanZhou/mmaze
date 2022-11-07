import random

from mmaze.generator.base import BaseMazeGenerator
from mmaze.maze import Maze
from mmaze.cell import CellType

RANDOM = 1
SERPENTINE = 2


class Wilsons(BaseMazeGenerator):
    """The Algorithm

    1. Choose a random cell and add it to the Uniform Spanning Tree (UST).
    2. Select any cell that is not in the UST and perform a random walk until you find a cell that is.
    3. Add the cells and walls visited in the random walk to the UST.
    4. Repeat steps 2 and 3 until all cells have been added to the UST.
    """
    symmetry_ok = False

    def __init__(self, hunt_order="random"):
        super().__init__()

        # the user can define what order to hunt for the next cell in
        if hunt_order.lower().strip() == "serpentine":
            self._hunt_order = SERPENTINE
        else:
            self._hunt_order = RANDOM

    def _generate(self, width: int, height: int, **kwargs) -> Maze:
        m = Maze(width, height, CellType.WALL)
        # find an arbitrary starting position
        row, col = m.random_position()
        m.set(row, col, CellType.ROAD)
        num_visited = 1
        row, col = self._hunt(m, num_visited)

        # perform many random walks, to fill the maze
        while row != -1 and col != -1:
            walk = self._generate_random_walk(m, (row, col))
            num_visited += self._solve_random_walk(m, walk, (row, col))
            row, col = self._hunt(m, num_visited)

        return m

    def _hunt(self, maze: Maze, count):
        """Based on how this algorithm was configured, choose hunt for the next starting point.

        Args:
            count (int): max number of times to iterate
        Returns:
            tuple: next cell
        """
        if self._hunt_order == SERPENTINE:
            return self._hunt_serpentine(maze, count)
        else:
            return self._hunt_random(maze, count)

    @staticmethod
    def _hunt_random(maze: Maze, count):
        """Select the next cell to walk from, randomly.

        Args:
            count (int): max number of times to iterate
        Returns:
            tuple: next cell
        """
        if count >= maze.base_width * maze.base_height:
            return -1, -1

        return maze.random_position()

    @staticmethod
    def _hunt_serpentine(maze: Maze, count):
        """Select the next cell to walk from by cycling through every grid cell in order.

        Args:
            count (int): max number of times to iterate
        Returns:
            tuple: next cell
        """
        cell = (1, -1)
        found = False

        while not found:
            cell = (cell[0], cell[1] + 2)
            if cell[1] > maze.width - 2:
                cell = (cell[0] + 2, 1)
                if cell[0] > maze.height - 2:
                    return -1, -1

            if maze.get(cell[0], cell[1]) != CellType.ROAD:
                found = True

        return cell

    def _generate_random_walk(self, maze: Maze, start):
        """From a given starting position, walk randomly until you hit a visited cell.

        The returned walk object is a dictionary mapping your location (cell) to a
        direction. If you randomly walk over the same cell twice, you overwrite
        the direction at that location.

        Args:
            maze (Maze): maze array
            start (tuple): position to start from
        Returns:
            dict: map of your location to the direction you want to travel
        """
        direction = self._random_dir(maze.width, maze.height, start)
        walk = {start: direction}
        current = self._move(start, direction)

        while maze.get(current[0], current[1]) == CellType.WALL:
            direction = self._random_dir(maze.width, maze.height, current)
            walk[current] = direction
            current = self._move(current, direction)

        return walk

    @staticmethod
    def _random_dir(width, height, current):
        """Take a step on one random (but valid) direction

        Args:
            current (tuple): cell to start from
        Returns:
            tuple: random, valid direction to travel to
        """
        r, c = current
        options = []
        if r > 1:
            options.append(0)  # North
        if r < (height - 2):
            options.append(1)  # South
        if c > 1:
            options.append(2)  # East
        if c < (width - 2):
            options.append(3)  # West

        direction = random.choice(options)
        if direction == 0:
            return -2, 0  # North
        elif direction == 1:
            return 2, 0  # South
        elif direction == 2:
            return 0, -2  # East
        else:
            return 0, 2  # West

    @staticmethod
    def _move(start, direction):
        """Convolve a position tuple with a direction tuple to generate a new position.

        Args:
            start (tuple): position to start from
            direction (tuple): vector direction to travel to
        Returns:
            tuple: position of next cell to travel to
        """
        return start[0] + direction[0], start[1] + direction[1]

    def _solve_random_walk(self, maze: Maze, walk, start):
        """Move through the random walk, visiting all the cells you touch,
        and breaking down the walls you cross.

        Args:
            walk (dict): random walk directions, from each cell
            start (tuple): position of cell to star the process at
        Returns:
            int: number of steps taken to complete the process
        """
        visits = 0
        current = start

        while maze.get(current[0], current[1]) != CellType.ROAD:
            maze.set(current[0], current[1], CellType.ROAD)
            next1 = self._move(current, walk[current])
            maze.set((next1[0] + current[0]) // 2, (next1[1] + current[1]) // 2, CellType.ROAD)
            visits += 1
            current = next1

        return visits
