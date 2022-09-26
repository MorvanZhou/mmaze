from abc import ABCMeta, abstractmethod

from mmaze.maze import Maze


class BaseMazeGenerator(metaclass=ABCMeta):

    @abstractmethod
    def generate(self, width: int, height: int) -> Maze:
        ...
