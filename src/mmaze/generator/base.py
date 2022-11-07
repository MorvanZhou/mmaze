import logging
from abc import ABCMeta, abstractmethod

from mmaze.maze import Maze
from mmaze.cell import CellType


class BaseMazeGenerator(metaclass=ABCMeta):
    symmetry_ok: bool

    def generate(self, width: int, height: int, symmetry: str = "none"):
        if symmetry not in ("n", "none") and not self.symmetry_ok:
            raise ValueError("symmetry must be 'none' for this generator, "
                             "or you can use backtracking/growingtree/huntandkill/prims"
                             " to generate symmetric maze")
        if self.symmetry_ok:
            if symmetry[0].lower() == "v" and height % 2 == 0:
                logging.warning("if with vertical symmetry, height must be odd number to ensure maze connection.")
            elif symmetry[0].lower() == "h" and width % 2 == 0:
                logging.warning("if with horizontal symmetry, width must be odd number to ensure maze connection.")
            elif symmetry[0].lower() == "b" and width % 2 == 0 and height % 2 == 0:
                logging.warning("if with both vertical and horizontal symmetry,"
                                " height and width must be odd number to ensure maze connection.")

            return self._generate(width, height, symmetry=symmetry)
        return self._generate(width, height)

    @abstractmethod
    def _generate(self, width: int, height: int, **kwargs) -> Maze:
        ...


def set_cell(m: Maze, pos: tuple, cell_type: CellType, symmetry: str, keep: list = None, remove: list = None) -> list:
    m.set(pos[0], pos[1], cell_type)
    new_set = {(pos[0], pos[1])}
    if symmetry in ("none", "n"):
        pass
    elif symmetry in ("vertical", "v"):
        r, c = m.height - 1 - pos[0], pos[1]
        m.set(r, c, cell_type)
        new_set.add((r, c))
    elif symmetry in ("horizontal", "h"):
        r, c = pos[0], m.width - 1 - pos[1]
        m.set(r, c, cell_type)
        new_set.add((r, c))
    elif symmetry in ("both", "b"):
        r1, c1 = m.height - 1 - pos[0], m.width - 1 - pos[1]
        m.set(r1, c1, cell_type)
        r2, c2 = m.height - 1 - pos[0], pos[1]
        m.set(r2, c2, cell_type)
        r3, c3 = pos[0], m.width - 1 - pos[1]
        m.set(r3, c3, cell_type)
        new_set.update({(r1, c1), (r2, c2), (r3, c3)})
    else:
        raise ValueError(
            f"symmetry must be one of "
            f"[\"horizontal\", \"vertical\", \"both\", \"none\"], but got {symmetry}")
    if keep is not None:
        tmp = set(keep)
        tmp.update(new_set)
        keep[:] = list(tmp)
    if remove is not None:
        for n in new_set:
            try:
                remove.remove(n)
            except ValueError:
                continue
    return list(new_set)
