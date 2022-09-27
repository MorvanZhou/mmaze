from enum import Enum


class CellType(Enum):
    ROAD = 0
    WALL = 1
    START = 2
    END = 3
    SOLUTION = 4
