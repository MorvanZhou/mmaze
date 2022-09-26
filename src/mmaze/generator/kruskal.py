import random
import typing as tp

from mmaze.generator.base import BaseMazeGenerator
from mmaze.maze import Maze


class Kruskal(BaseMazeGenerator):
    def __init__(self):
        super().__init__()

    def generate(self, width: int, height: int) -> Maze:
        m = Maze(width, height, 1)
        forest = []
        for row in range(1, m.height - 1, 2):
            for col in range(1, m.width - 1, 2):
                forest.append([(row, col)])
                m.set(row, col, 0)

        edges: tp.List[tp.Tuple[int, int]] = []
        for row in range(2, m.height - 1, 2):
            for col in range(1, m.width - 1, 2):
                edges.append((row, col))
        for row in range(1, m.height - 1, 2):
            for col in range(2, m.width - 1, 2):
                edges.append((row, col))

        random.shuffle(edges)

        while len(forest) > 1:
            ce_row, ce_col = edges[0]
            edges = edges[1:]

            tree1 = -1
            tree2 = -1

            if ce_row % 2 == 0:  # even-numbered row: vertical wall
                tree1 = sum(
                    [
                        i if (ce_row - 1, ce_col) in j else 0
                        for i, j in enumerate(forest)
                    ]
                )
                tree2 = sum(
                    [
                        i if (ce_row + 1, ce_col) in j else 0
                        for i, j in enumerate(forest)
                    ]
                )
            else:  # odd-numbered row: horizontal wall
                tree1 = sum(
                    [
                        i if (ce_row, ce_col - 1) in j else 0
                        for i, j in enumerate(forest)
                    ]
                )
                tree2 = sum(
                    [
                        i if (ce_row, ce_col + 1) in j else 0
                        for i, j in enumerate(forest)
                    ]
                )

            if tree1 != tree2:
                new_tree = forest[tree1] + forest[tree2]
                temp1 = list(forest[tree1])
                temp2 = list(forest[tree2])
                forest = [
                    x for x in forest if x != temp1
                ]  # faster than forest.remove(temp1)
                forest = [x for x in forest if x != temp2]
                forest.append(new_tree)
                m.set(ce_row, ce_col, 0)

        return m
