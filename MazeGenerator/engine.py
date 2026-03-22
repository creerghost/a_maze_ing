from typing import List, Optional, Tuple
from MazeGenerator.generator import MazeGenerator
from MazeGenerator.renderer import MazeRenderer
from MazeGenerator.solver import MazeSolver


class MazeEngine:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit_coords: Tuple[int, int],
        output_file: str,
        perfect: bool,
        seed: int,
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit_coords: Tuple[int, int] = exit_coords
        self.output_file: str = output_file
        self.perfect: bool = perfect
        self.seed: int = seed
        self.renderer: MazeRenderer = MazeRenderer()
        self.solver: MazeSolver = MazeSolver(entry, exit_coords)
        self.grid: List[List[int]] = []
        self.path: str = ""

    def generate(self) -> None:
        config = {
            "WIDTH": str(self.width),
            "HEIGHT": str(self.height),
            "ENTRY": f"{self.entry[0]},{self.entry[1]}",
            "EXIT": f"{self.exit_coords[0]},{self.exit_coords[1]}",
            "OUTPUT_FILE": self.output_file,
            "PERFECT": "True" if self.perfect else "False",
            "SEED": str(self.seed),
        }
        generator = MazeGenerator(config)
        generator.generate()
        self.grid = generator.grid
        self.path = ""

    def solve(self) -> None:
        if not self.grid:
            self.generate()
        solution: Optional[str] = self.solver.solve(self.grid)
        self.path = solution if solution is not None else ""

    def save(self) -> None:
        config = {
            "WIDTH": str(self.width),
            "HEIGHT": str(self.height),
            "ENTRY": f"{self.entry[0]},{self.entry[1]}",
            "EXIT": f"{self.exit_coords[0]},{self.exit_coords[1]}",
            "OUTPUT_FILE": self.output_file,
            "PERFECT": "True" if self.perfect else "False",
            "SEED": str(self.seed),
        }
        generator = MazeGenerator(config)
        generator.grid = self.grid
        generator.save(self.entry, self.exit_coords, self.path)

    def show(self, with_path: bool = False) -> None:
        self.renderer.render(
            self.grid, self.entry, self.path, self.exit_coords, with_path
        )
