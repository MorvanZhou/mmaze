import random

from mmaze.generator.base import BaseMazeGenerator
from mmaze.maze import Maze, CellType

# CONSTANTS
VERTICAL = 0
HORIZONTAL = 1


class Division(BaseMazeGenerator):
    """
    1. Start with an empty grid.
    2. Build a wall that bisects the grid (horizontal or vertical). Add a single passage through the wall.
    3. Repeat step 2 with the areas on either side of the wall.
    4. Continue, recursively, until the maze passages are the desired resolution.
    """
    symmetry_ok = False

    def _generate(self, width: int, height: int, **kwargs):
        # create empty grid
        m = Maze(width, height, cell_type=CellType.ROAD)
        # fill borders
        m.data[0] = [CellType.WALL for _ in range(len(m.data[0]))]
        m.data[-1] = [CellType.WALL for _ in range(len(m.data[-1]))]
        for i in range(m.height):
            m.set(i, 0, CellType.WALL)
            m.set(i, -1, CellType.WALL)

        region_stack = [((1, 1), (m.height - 2, m.width - 2))]

        while region_stack:
            current_region = region_stack[-1]
            region_stack = region_stack[:-1]
            min_y = current_region[0][0]
            max_y = current_region[1][0]
            min_x = current_region[0][1]
            max_x = current_region[1][1]
            height = max_y - min_y + 1
            width = max_x - min_x + 1

            if height <= 1 or width <= 1:
                continue

            if width < height:
                cut_direction = HORIZONTAL  # with 100% chance
            elif width > height:
                cut_direction = VERTICAL  # with 100% chance
            else:
                if width == 2:
                    continue
                cut_direction = random.randrange(2)

            # MAKE CUT
            # select cut position (can't be completely on the edge of the region)
            cut_length = (height, width)[(cut_direction + 1) % 2]
            if cut_length < 3:
                continue
            cut_posi = random.randrange(1, cut_length, 2)
            # select new door position
            door_posi = random.randrange(0, (height, width)[cut_direction], 2)
            # add walls to correct places
            if cut_direction == 0:  # vertical
                for row in range(min_y, max_y + 1):
                    m.set(row, min_x + cut_posi, CellType.WALL)
                m.set(min_y + door_posi, min_x + cut_posi, CellType.ROAD)

                # add new regions to stack
                region_stack.append(((min_y, min_x), (max_y, min_x + cut_posi - 1)))
                region_stack.append(((min_y, min_x + cut_posi + 1), (max_y, max_x)))

            else:  # horizontal
                for col in range(min_x, max_x + 1):
                    m.set(min_y + cut_posi, col, CellType.WALL)
                m.set(min_y + cut_posi, min_x + door_posi, CellType.ROAD)

                # add new regions to stack
                region_stack.append(((min_y, min_x), (min_y + cut_posi - 1, max_x)))
                region_stack.append(((min_y + cut_posi + 1, min_x), (max_y, max_x)))

        return m
