# A-Maze-ing: Maze Generator and Solver

*This project has been created as part of the 42 curriculum.*

## Description

A-Maze-ing is a comprehensive maze generation and visualization project written in Python. It generates random mazes using industry-standard algorithms (Prim's and Depth-First Search), provides both perfect mazes (single path) and non-perfect mazes (multiple paths), and includes an interactive ASCII terminal visualizer with multiple color themes.

The project demonstrates practical applications of graph theory, randomization, and algorithm design. It generates mazes as hexadecimal-encoded cell data, ensures full connectivity, embeds a visible "42" pattern, and automatically solves generated mazes using Breadth-First Search.

## Features

- **Maze Generation**: Creates random mazes using Prim's and DFS algorithms
- **Perfect & Non-Perfect Modes**: Support for both single-path and multi-path mazes
- **Hexadecimal Output**: Compact representation of wall structure using bitwise encoding
- **ASCII Visualization**: Terminal-based rendering with 6 color themes
- **Path Solving**: Automatic shortest-path finding using BFS algorithm
- **Interactive Menu**: Generate new mazes, toggle solution visibility, switch themes
- **"42" Pattern**: Embeds a visible 7×5 pattern in maze visualization (when size permits)
- **Configuration-Driven**: All parameters controllable via config.txt
- **Reproducible**: Seed support for maze generation reproducibility
- **Reusable Module**: Code organized for import and reuse in other projects

## Instructions

### Installation

```bash
make install
```

This installs all dependencies listed in `requirements.txt`.

### Running the Program

```bash
make run
```

Or manually:

```bash
python3 a_maze_ing.py config.txt
```

### Debug Mode

```bash
make debug
```

Runs the program with Python's built-in debugger (pdb).

### Code Quality

```bash
make lint       # Run flake8 and mypy
make lint-strict # Run with strict mypy rules
make clean      # Remove cache files
```

## Configuration File Format

The `config.txt` file controls all maze generation parameters. Format: `KEY=VALUE` per line, lines starting with `#` are comments.

### Mandatory Keys

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | Maze height in cells | `HEIGHT=15` |
| `ENTRY` | Entry coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Perfect maze? (True/False) | `PERFECT=False` |

### Optional Keys

| Key | Description | Default |
|-----|-------------|---------|
| `SEED` | Random seed for reproducibility | `0` |
| `ALGORITHM` | Generation algorithm (prim/dfs) | `dfs` |

### Example Configuration

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=12345
ALGORITHM=dfs
```

## Output File Format

The output maze file uses hexadecimal encoding:

- **One hex digit per cell** (0-F), representing wall configuration
- **Bit encoding**:
  - Bit 0 (LSB): North wall
  - Bit 1: East wall
  - Bit 2: South wall
  - Bit 3: West wall
  - Bit=1 means wall closed, Bit=0 means open

- **Example**: 
  - `3` (binary `0011`) = North & East walls open, South & West walls closed
  - `A` (binary `1010`) = East & West walls closed, North & South walls open

- **File structure**:
  ```
  [Hex maze grid, one row per line]
  
  [Entry x,y]
  [Exit x,y]
  [Solution path as N/E/S/W moves]
  ```

## Interactive Menu

When running the program, use these commands:

| Command | Action |
|---------|--------|
| `g` | Generate a new maze (auto-saved) |
| `s` | Show/Hide solution path |
| `t` | Next color theme |
| `q` | Quit program |

### Color Themes

6 built-in themes with different wall and path colors:
1. Classic (cyan walls)
2. Sunset (yellow walls)
3. Ocean (blue walls)
4. Forest (green walls)
5. Crimson (red walls)
6. Purple (magenta walls)

## Maze Generation Algorithm

### Chosen Algorithm: Depth-First Search (DFS) with Cycle Addition

**Why DFS?**
- Simple and elegant implementation
- Produces mazes with longer, more complex corridors
- Low memory overhead (stack-based)
- Excellent for educational purposes
- Generates interesting maze patterns

**Perfect Mazes (PERFECT=True)**:
- Pure tree-based generation using DFS
- Guarantees exactly one path between any two points
- Single spanning tree of the grid graph

**Non-Perfect Mazes (PERFECT=False)**:
- DFS generates perfect base maze
- Additional cycles added randomly (~1 per 20 cells)
- Creates alternative paths and puzzle complexity
- Can result in shorter solution paths

**Algorithm Steps**:
1. Initialize all cells with all walls closed (value 15)
2. Start DFS from (0,0)
3. For each cell: carve randomly to unvisited neighbors
4. Recursively visit carved neighbor cells
5. If non-perfect: randomly open additional walls to create loops

**Complexity**: O(width × height) time and space

## Reusable Module

### MazeGenerator Class

The core maze generation logic is encapsulated in a reusable module. Import and use it in your own projects:

```python
from MazeGenerator.generator import MazeGenerator
from MazeGenerator.solver import MazeSolver

# Configure the maze
config = {
    "WIDTH": "25",
    "HEIGHT": "20",
    "ENTRY": "0,0",
    "EXIT": "24,19",
    "OUTPUT_FILE": "my_maze.txt",
    "PERFECT": "True",
    "SEED": "42",
    "ALGORITHM": "prim"
}

# Generate maze
generator = MazeGenerator(config)
generator.generate()

# Access the grid (list of lists, values 0-15)
grid = generator.grid
width = generator.width
height = generator.height

# Save to file
generator.save(entry=(0,0), exit_coords=(24,19), solution_path="SSSEEEEE...")

# Solve the maze
solver = MazeSolver(start=(0,0), end=(24,19))
path = solver.solve(grid)  # Returns "NESW..." string or None
```

### API Reference

#### MazeGenerator

```python
class MazeGenerator:
    def __init__(self, config: Dict[str, str]) -> None:
        """Initialize generator with configuration dictionary."""
    
    def generate(self) -> None:
        """Generate the maze."""
    
    def save(self, entry: Tuple[int, int], exit_coords: Tuple[int, int], 
             solution_path: str = "") -> None:
        """Save maze to output file in hexadecimal format."""
```

#### MazeSolver

```python
class MazeSolver:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        """Initialize solver with start and end coordinates."""
    
    def solve(self, grid: List[List[int]]) -> Optional[str]:
        """Find shortest path using BFS. Returns 'NESW' string or None."""
```

#### MazeEngine (High-Level Orchestrator)

```python
class MazeEngine:
    def __init__(self, width: int, height: int, entry: Tuple[int, int],
                 exit_coords: Tuple[int, int], output_file: str,
                 perfect: bool, seed: int) -> None:
        """Initialize complete maze system."""
    
    def generate(self) -> None:
        """Generate maze."""
    
    def solve(self) -> None:
        """Solve maze and store path."""
    
    def show(self, with_path: bool = False) -> None:
        """Display maze in terminal with optional solution path."""
    
    def switch_theme(self) -> None:
        """Cycle to next color theme."""
```

### Code Reusability Structure

The project is organized into logical, importable modules:

- **`MazeGenerator/generator.py`**: Core generation engine, configuration parsing, I/O
- **`MazeGenerator/algorithms.py`**: Prim's and DFS maze algorithms (easily extensible)
- **`MazeGenerator/solver.py`**: BFS pathfinding algorithm
- **`MazeGenerator/renderer.py`**: ASCII visualization with color themes
- **`MazeGenerator/engine.py`**: High-level orchestrator combining all components
- **`MazeGenerator/parser.py`**: Configuration file parsing utilities
- **`MazeGenerator/validator.py`**: Input validation helpers

Each module is independent and can be imported separately. The main `a_maze_ing.py` script demonstrates integration.

## Requirements & Constraints

### Maze Requirements Met

✅ **Randomly generated with seed support** - All mazes reproducible via SEED parameter

✅ **Cell wall structure** - Each cell 0-4 walls (N/E/S/W)

✅ **Valid maze guarantees**:
- Entry and exit exist at grid boundaries
- Full connectivity (no isolated cells except "42" pattern)
- External border walls enforced
- Neighbor wall coherence (bidirectional wall updates)

✅ **Corridor width constraint** - Algorithms prevent >2 cell wide open areas

✅ **"42" pattern** - 7×5 blocked cell pattern embedded when maze ≥9×7

✅ **Perfect maze support** - PERFECT flag controls single vs multi-path

### Technical Standards Met

✅ **Python 3.10+** - Type hints throughout

✅ **flake8 & mypy** - Passes all linting and static type checks

✅ **Error handling** - Graceful exception handling, clear error messages

✅ **Resource management** - Proper context managers for file I/O

✅ **Docstrings** - PEP 257 compliant documentation

✅ **Makefile** - All required rules (install, run, debug, clean, lint, lint-strict)

## Team & Project Management

**Solo Project** - Completed independently

### Development Approach

1. **Phase 1**: Understanding & Algorithm Selection
   - Studied maze generation theory
   - Evaluated Prim's vs DFS vs other algorithms
   - Selected DFS for elegance and educational value

2. **Phase 2**: Core Implementation
   - Implemented hexadecimal wall encoding
   - Built DFS and Prim's algorithms
   - Added "42" pattern detection and blocking

3. **Phase 3**: Output & Validation
   - Implemented output file format
   - Added configuration parsing
   - Created maze validation

4. **Phase 4**: Visualization & Interactivity
   - Built ASCII renderer with color themes
   - Implemented interactive menu
   - Added path visualization

5. **Phase 5**: Solver Integration
   - Implemented BFS pathfinding
   - Integrated solver with renderer
   - Tested path display

6. **Phase 6**: Non-Perfect Mazes & Polish
   - Added cycle generation for non-perfect mazes
   - Fixed renderer path display bug
   - Final testing and code cleanup

### What Worked Well

✅ **Hexadecimal encoding** - Elegant, compact representation

✅ **Modular architecture** - Each component independent and testable

✅ **DFS algorithm** - Simple yet effective, easy to extend

✅ **BFS solver** - Optimal pathfinding, reliable

✅ **ANSI colors** - Terminal rendering with multiple themes

✅ **Configuration-driven design** - Flexible, easy to test different parameters

### Could Be Improved

⚠️ **Animation during generation** - Could show real-time maze carving

⚠️ **Alternative visualization** - MLX graphical library not implemented

⚠️ **Kruskal's algorithm** - Could add as second algorithm option

⚠️ **Maze statistics** - Could track and display metrics (path length, branching factor)

⚠️ **Performance optimization** - Could use numpy for very large mazes

## Tools & Technologies Used

- **Python 3.10+**: Main language
- **ANSI escape codes**: Terminal color rendering
- **Standard library only**: No external dependencies for core functionality
- **Git**: Version control
- **Makefile**: Build automation
- **flake8 & mypy**: Code quality

### AI Usage

AI was used primarily for:
- **Code structure guidance** - Architectural patterns and module organization
- **Bug debugging** - Identifying issues in wall rendering and path visualization
- **Documentation** - Generating comprehensive docstrings and README sections
- **Validation logic** - Input checking and error message formatting

All AI-generated code was thoroughly reviewed, tested, and understood before integration. No code was blindly copied.

## Resources & References

### Maze Generation Theory

- [Maze Generation Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracker Algorithm](http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Prim's Algorithm for Maze Generation](http://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm)
- [Think Complexity - Chapter 2 (Graph Algorithms)](https://greenteapress.com/thinkcomplex/)

### Graph Theory & Data Structures

- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) - Chapters on BFS/DFS
- [Spanning Trees & Perfect Mazes](https://en.wikipedia.org/wiki/Spanning_tree)

### Python Best Practices

- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [PEP 8 - Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Type Hints Guide](https://docs.python.org/3/library/typing.html)
- [mypy Documentation](http://mypy-lang.org/)

### Testing & Quality

- [pytest Documentation](https://docs.pytest.org/)
- [flake8 Linter](https://flake8.pycqa.org/)

## License

This project is part of the 42 curriculum.

## Acknowledgments

Special thanks to the 42 curriculum for the engaging project brief and inspiration from the legendary Labyrinth of Knossos.
