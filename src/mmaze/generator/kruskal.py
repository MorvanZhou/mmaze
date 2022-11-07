import random
import typing as tp

from mmaze.generator.base import BaseMazeGenerator
from mmaze.maze import Maze
from mmaze.cell import CellType


class Kruskal(BaseMazeGenerator):
    symmetry_ok = False

    def _generate(self, width: int, height: int, **kwargs) -> Maze:
        m = Maze(width, height, CellType.WALL)
        forest = []
        for row in range(1, m.height - 1, 2):
            for col in range(1, m.width - 1, 2):
                forest.append([(row, col)])
                m.set(row, col, CellType.ROAD)

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
                m.set(ce_row, ce_col, CellType.ROAD)

        return m

    @staticmethod
    def _step(ce_row, ce_col, forest, m):
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
            m.set(ce_row, ce_col, CellType.ROAD)
            return True
        return False
