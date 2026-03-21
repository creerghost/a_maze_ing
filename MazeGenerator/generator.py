import random
from typing import Dict, List
from maze_generator.algorithms import MazeAlgorithm, PrimAlgorithm


class MazeGenerator:
    def __init__(self, config: Dict[str, str]) -> None:
        self.width: int = int(config["WIDTH"])
        self.height: int = int(config["HEIGHT"])
        self.perfect: int = int(config.get["PERFECT",
                                           "False"].lower() == "true")
        self.seed: str | None = config.get("SEED")
        if self.seed:
            random.seed(self.seed)
        self.grid: List[List[int]] = [[15 for _ in range(self.width)]
                                      for _ in range(self.height)]
        self.is_42: List[List[bool]] = [[False for _ in range(self.width)]
                                        for _ in range(self.height)]
        algo_name = config.get("ALGORITHM", "backtracker").lower()
        self.strategy: MazeAlgorithm = self._get_strategy(algo_name)
