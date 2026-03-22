from abc import ABC, abstractmethod
from typing import List, Set, Tuple
import random


class MazeAlgorithm(ABC):
    N: int = 1
    E: int = 2
    S: int = 4
    W: int = 8

    @abstractmethod
    def dig_maze(self, grid: List[List[int]], width: int, height: int,
                 blocked: Set[Tuple[int, int]], perfect: bool) -> None:
        pass

    def _open(self, grid: List[List[int]], c1: Tuple[int, int],
              c2: Tuple[int, int], d: int) -> None:
        grid[c1[1]][c1[0]] &= ~d
        rev: int = self.E
        if d == self.N:
            rev = self.S
        elif d == self.S:
            rev = self.N
        elif d == self.E:
            rev = self.W
        grid[c2[1]][c2[0]] &= ~rev

    def _is_valid(self, x: int, y: int, width: int, height: int,
                  blocked: Set[Tuple[int, int]]) -> bool:
        return 0 <= x < width and 0 <= y < height and (x, y) not in blocked


class PrimAlgorithm(MazeAlgorithm):
    def dig_maze(self, grid: List[List[int]], width: int, height: int,
                 blocked: Set[Tuple[int, int]], perfect: bool) -> None:
        if width == 0 or height == 0:
            return

        start_x, start_y = 0, 0
        visited: Set[Tuple[int, int]] = set()
        visited.add((start_x, start_y))

        walls: Set[Tuple[Tuple[int, int], Tuple[int, int], int]] = set()
        self._add_walls(walls, start_x, start_y, width, height, visited,
                        blocked)

        while walls:
            (cx, cy), (nx, ny), direction = random.choice(list(walls))
            walls.discard(((cx, cy), (nx, ny), direction))

            if (nx, ny) not in visited:
                visited.add((nx, ny))
                self._open(grid, (cx, cy), (nx, ny), direction)
                self._add_walls(walls, nx, ny, width, height, visited,
                                blocked)

        if not perfect:
            self._add_cycles(grid, width, height, blocked)

    def _add_walls(self, walls: Set[Tuple[Tuple[int, int], Tuple[int, int],
                                          int]], x: int, y: int, width: int,
                   height: int, visited: Set[Tuple[int, int]],
                   blocked: Set[Tuple[int, int]]) -> None:
        for dx, dy, d in [(0, -1, self.N), (1, 0, self.E), (0, 1, self.S),
                          (-1, 0, self.W)]:
            nx, ny = x + dx, y + dy
            if self._is_valid(nx, ny, width, height, blocked) and \
                    (nx, ny) not in visited:
                walls.add(((x, y), (nx, ny), d))

    def _add_cycles(self, grid: List[List[int]], width: int, height: int,
                    blocked: Set[Tuple[int, int]]) -> None:
        num_cycles = max(1, (width * height) // 20)
        for _ in range(num_cycles):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            if (x, y) not in blocked:
                for dx, dy, d in [(0, -1, self.N), (1, 0, self.E),
                                  (0, 1, self.S), (-1, 0, self.W)]:
                    nx, ny = x + dx, y + dy
                    if self._is_valid(nx, ny, width, height, blocked):
                        if random.random() < 0.3:
                            self._open(grid, (x, y), (nx, ny), d)


class DFSAlgorithm(MazeAlgorithm):
    def dig_maze(self, grid: List[List[int]], width: int, height: int,
                 blocked: Set[Tuple[int, int]], perfect: bool) -> None:
        if width == 0 or height == 0:
            return

        start_x, start_y = 0, 0
        self._dfs_iterative(grid, start_x, start_y, width, height, blocked)

        if not perfect:
            self._add_cycles_smart(grid, width, height, blocked)

    def _dfs_iterative(self, grid: List[List[int]], start_x: int,
                       start_y: int, width: int, height: int,
                       blocked: Set[Tuple[int, int]]) -> None:
        visited: Set[Tuple[int, int]] = set()
        stack: List[Tuple[Tuple[int, int], List[Tuple[int, int, int]]]] = []

        current = (start_x, start_y)
        visited.add(current)

        while True:
            x, y = current
            neighbors: List[Tuple[int, int, int]] = []
            for dx, dy, d in [(0, -1, self.N), (1, 0, self.E),
                              (0, 1, self.S), (-1, 0, self.W)]:
                nx, ny = x + dx, y + dy
                if self._is_valid(nx, ny, width, height, blocked) and \
                        (nx, ny) not in visited:
                    neighbors.append((nx, ny, d))

            if neighbors:
                random.shuffle(neighbors)
                next_x, next_y, direction = neighbors[0]
                remaining = neighbors[1:]
                stack.append((current, remaining))
                self._open(grid, current, (next_x, next_y), direction)
                visited.add((next_x, next_y))
                current = (next_x, next_y)
            elif stack:
                current, remaining_neighbors = stack.pop()
                while remaining_neighbors:
                    next_x, next_y, direction = remaining_neighbors.pop(0)
                    if (next_x, next_y) not in visited:
                        visited.add((next_x, next_y))
                        self._open(grid, current, (next_x, next_y), direction)
                        current = (next_x, next_y)
                        break
                else:
                    if not stack:
                        break
            else:
                break

    def _add_cycles_smart(self, grid: List[List[int]], width: int,
                          height: int,
                          blocked: Set[Tuple[int, int]]) -> None:
        cells_to_connect = list(range(width * height))
        random.shuffle(cells_to_connect)

        num_cycles = max(1, (width * height) // 20)
        cycles_added = 0

        for cell_idx in cells_to_connect:
            if cycles_added >= num_cycles:
                break

            x = cell_idx % width
            y = cell_idx // width

            if (x, y) in blocked:
                continue

            neighbors: List[Tuple[int, int, int]] = []
            for dx, dy, d in [(0, -1, self.N), (1, 0, self.E),
                              (0, 1, self.S), (-1, 0, self.W)]:
                nx, ny = x + dx, y + dy
                if self._is_valid(nx, ny, width, height, blocked):
                    if (grid[y][x] & d) != 0:
                        neighbors.append((nx, ny, d))

            if neighbors:
                nx, ny, d = neighbors[0]
                self._open(grid, (x, y), (nx, ny), d)
                cycles_added += 1
