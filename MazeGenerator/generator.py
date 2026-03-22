import random
from typing import Dict, List, Set, Tuple
from MazeGenerator.algorithms import MazeAlgorithm, PrimAlgorithm, DFSAlgorithm


class MazeGenerator:
    PATTERN: List[List[int]] = [
        [1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1],
    ]
    P_H: int = 5
    P_W: int = 7

    def __init__(self, config: Dict[str, str]) -> None:
        self.width: int = int(config["WIDTH"])
        self.height: int = int(config["HEIGHT"])
        self.perfect: bool = config.get("PERFECT",
                                        "False").lower() == "true"
        self.seed: int = int(config.get("SEED", "0"))
        self.output_file: str = config.get("OUTPUT_FILE", "maze.txt")
        random.seed(self.seed)
        self.grid: List[List[int]] = [[15 for _ in range(self.width)]
                                      for _ in range(self.height)]
        self.blocked: Set[Tuple[int, int]] = set()
        self._check_pattern_fit()
        algo_name = config.get("ALGORITHM", "backtracker").lower()
        self.strategy: MazeAlgorithm = self._get_strategy(algo_name)

    def _check_pattern_fit(self) -> None:
        can_fit = self.width >= 9 and self.height >= 7
        if can_fit:
            off_x = (self.width - self.P_W) // 2
            off_y = (self.height - self.P_H) // 2
            for py in range(self.P_H):
                for px in range(self.P_W):
                    if self.PATTERN[py][px] == 1:
                        self.blocked.add((off_x + px, off_y + py))
        else:
            print("Error: Maze size too small for '42' pattern. "
                  "Pattern will be omitted.")

    def _is_blocked(self, x: int, y: int) -> bool:
        return (x, y) in self.blocked

    def _get_strategy(self, algo_name: str) -> MazeAlgorithm:
        if algo_name == "prim":
            return PrimAlgorithm()
        elif algo_name == "dfs":
            return DFSAlgorithm()
        else:
            return DFSAlgorithm()

    def generate(self) -> None:
        self.strategy.dig_maze(self.grid, self.width, self.height,
                               self.blocked, self.perfect)

    def save(self, entry: tuple[int, int] | None = None,
             exit_coords: tuple[int, int] | None = None,
             solution_path: str = "") -> None:
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for row in self.grid:
                line = ""
                for cell in row:
                    line += f"{cell:X}"
                f.write(line + "\n")

            if entry is not None and exit_coords is not None:
                f.write("\n")
                f.write(f"{entry[0]},{entry[1]}\n")
                f.write(f"{exit_coords[0]},{exit_coords[1]}\n")
                f.write(f"{solution_path}\n")
