from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Theme:
    name: str
    wall_color: str
    path_color: str


class MazeRenderer:
    RATIO: int = 2
    BLOCK: str = "█"
    SHADE: str = "░"
    EMPTY: str = " "

    THEMES: List[Theme] = [
        Theme("Classic", "\033[97m", "\033[91m"),
        Theme("Hell", "\033[91m", "\033[93m"),
        Theme("Forest", "\033[92m", "\033[95m"),
        Theme("Cyber", "\033[93m", "\033[94m"),
        Theme("Deep Sea", "\033[94m", "\033[96m"),
        Theme("Neon", "\033[95m", "\033[92m"),
    ]

    VOID_C: str = "\033[90m"
    STRT_C: str = "\033[92m"
    EXIT_C: str = "\033[96m"
    RESET: str = "\033[0m"

    def __init__(self) -> None:
        self._current_theme_index: int = 0

    def next_theme(self) -> str:
        self._current_theme_index = (
            self._current_theme_index + 1
        ) % len(self.THEMES)
        return self.THEMES[self._current_theme_index].name

    def get_current_theme_name(self) -> str:
        return self.THEMES[self._current_theme_index].name

    def _fill_cell(
        self,
        canvas: List[List[str]],
        tx: int,
        ty: int,
        char: str,
        color: str = "",
    ) -> None:
        fmt: str = f"{color}{char}{self.RESET}" if color else char
        for dx in range(self.RATIO):
            canvas[ty][tx * self.RATIO + dx] = fmt

    def render(
        self,
        grid: List[List[int]],
        start: Tuple[int, int],
        path_str: str = "",
        end_coords: Optional[Tuple[int, int]] = None,
        show_path: bool = False,
    ) -> None:
        if not grid or not grid[0]:
            return

        theme: Theme = self.THEMES[self._current_theme_index]
        height: int = len(grid)
        width: int = len(grid[0])
        canvas_w: int = width * 2 + 1
        canvas_h: int = height * 2 + 1

        default_wall: str = f"{theme.wall_color}{self.BLOCK}{self.RESET}"
        canvas: List[List[str]] = [
            [default_wall for _ in range(canvas_w * self.RATIO)]
            for _ in range(canvas_h)
        ]

        for y in range(height):
            for x in range(width):
                cell: int = grid[y][x]
                cx: int = x * 2 + 1
                cy: int = y * 2 + 1

                if cell == 15:
                    self._fill_cell(canvas, cx, cy, self.SHADE, self.VOID_C)
                else:
                    self._fill_cell(canvas, cx, cy, self.EMPTY)

                if not (cell & 1):
                    self._fill_cell(canvas, cx, cy - 1, self.EMPTY)
                if not (cell & 2):
                    self._fill_cell(canvas, cx + 1, cy, self.EMPTY)
                if not (cell & 4):
                    self._fill_cell(canvas, cx, cy + 1, self.EMPTY)
                if not (cell & 8):
                    self._fill_cell(canvas, cx - 1, cy, self.EMPTY)

        curr_x: int = start[0] * 2 + 1
        curr_y: int = start[1] * 2 + 1

        if show_path and path_str:
            moves: Dict[str, Tuple[int, int]] = {
                "N": (0, -1),
                "S": (0, 1),
                "E": (1, 0),
                "W": (-1, 0),
            }
            self._fill_cell(
                canvas, curr_x, curr_y, self.BLOCK, theme.path_color
            )
            for move in path_str:
                dx, dy = moves[move]
                self._fill_cell(
                    canvas,
                    curr_x + dx,
                    curr_y + dy,
                    self.BLOCK,
                    theme.path_color,
                )
                curr_x += dx * 2
                curr_y += dy * 2
                self._fill_cell(
                    canvas, curr_x, curr_y, self.BLOCK, theme.path_color
                )

        start_cx: int = start[0] * 2 + 1
        start_cy: int = start[1] * 2 + 1
        self._fill_cell(canvas, start_cx, start_cy, self.BLOCK, self.STRT_C)

        if end_coords:
            ex, ey = end_coords[0] * 2 + 1, end_coords[1] * 2 + 1
        else:
            ex, ey = curr_x, curr_y

        self._fill_cell(canvas, ex, ey, self.BLOCK, self.EXIT_C)

        for row in canvas:
            print("".join(row))
