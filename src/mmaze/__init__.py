import typing as tp

from mmaze import generator
from mmaze import solver
from mmaze import visual
from mmaze.maze import Maze
from mmaze.generator.base import BaseMazeGenerator
from mmaze.solver.base import BaseSolver


__GENERATOR_MAP: tp.Dict[str, tp.Type[BaseMazeGenerator]] = {}
__BASE_GENERATOR_MODULE = BaseMazeGenerator.__module__
__SOLVER_MAP: tp.Dict[str, tp.Type[BaseSolver]] = {}
__BASE_SOLVER_MODULE = BaseSolver.__module__


def _set_generator_map(cls, m: dict):
    for subclass in cls.__subclasses__():
        if subclass.__module__ != __BASE_GENERATOR_MODULE:
            m[subclass.__name__.lower()] = subclass
        else:
            raise ValueError(f"module name exists, cannot put twice. {subclass.__name__.lower()}")
        _set_generator_map(subclass, m)


def _set_solver_map(cls, m: dict):
    for subclass in cls.__subclasses__():
        if subclass.__module__ != __BASE_SOLVER_MODULE:
            m[subclass.__name__.lower()] = subclass
        else:
            raise ValueError(f"module name exists, cannot put twice. {subclass.__name__.lower()}")
        _set_solver_map(subclass, m)


def generate(width: int, height: int, method: str = "backtracking") -> Maze:
    if len(__GENERATOR_MAP) == 0:
        _set_generator_map(BaseMazeGenerator, __GENERATOR_MAP)
    try:
        g = __GENERATOR_MAP[method.lower()]()
    except KeyError as e:
        raise ValueError(f"method of '{method}' is not found, try one of {list(__GENERATOR_MAP.keys())}: {e}")
    return g.generate(width=width, height=height)


def solve(maze: "Maze", start: tp.Sequence[int], end: tp.Sequence[int], method: str = "backtracking") -> tp.List:
    if len(__SOLVER_MAP) == 0:
        _set_solver_map(BaseSolver, __SOLVER_MAP)
    try:
        s = __SOLVER_MAP[method.lower()]()
    except KeyError as e:
        raise ValueError(f"method of '{method}' is not found, try one of {list(__SOLVER_MAP.keys())}: {e}")
    return s.solve(maze=maze, start=start, end=end)
