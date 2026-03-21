from abc import ABC, abstractmethod
from typing import List


class MazeAlgorithm(ABC):
    @abstractmethod
    def dig_maze(self, grid: List[List[int]], is_42: List[List[bool]],
                 width: int, height: int) -> None:
        pass


class PrimAlgorithm(MazeAlgorithm):
    def dig_maze(self, grid: List[List[int]], is_42: List[List[bool]],
                 width: int, height: int) -> None:
        # TODO: Prim's logic.
        pass


class DFSAlgorithm(MazeAlgorithm):
    def dig_maze(self, grid: List[List[int]], is_42: List[List[bool]],
                 width: int, height: int) -> None:
        # TODO: Prim's logic.
        pass
