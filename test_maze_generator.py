import pytest
import os
import tempfile
from MazeGenerator.parser import Parser
from MazeGenerator.validator import Validator
from MazeGenerator.generator import MazeGenerator
from MazeGenerator.algorithms import PrimAlgorithm, DFSAlgorithm


class TestParser:
    def test_parse_valid_config(self) -> None:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt',
                                         delete=False) as f:
            f.write("WIDTH=20\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\n")
            f.flush()
            parser = Parser(f.name)
            config = parser.parse()
            assert config["WIDTH"] == "20"
            assert config["HEIGHT"] == "15"
            assert config["ENTRY"] == "0,0"
            os.unlink(f.name)

    def test_parse_nonexistent_file(self) -> None:
        parser = Parser("/nonexistent/file.txt")
        with pytest.raises(FileNotFoundError):
            parser.parse()

    def test_parse_invalid_syntax(self) -> None:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt',
                                         delete=False) as f:
            f.write("INVALID_LINE\n")
            f.flush()
            parser = Parser(f.name)
            with pytest.raises(ValueError):
                parser.parse()
            os.unlink(f.name)


class TestValidator:
    def test_validate_valid_config(self) -> None:
        config = {
            "WIDTH": "20",
            "HEIGHT": "15",
            "ENTRY": "0,0",
            "EXIT": "19,14",
            "OUTPUT_FILE": "maze.txt",
            "PERFECT": "True"
        }
        validator = Validator(config)
        validator.validate()

    def test_validate_missing_keys(self) -> None:
        config = {"WIDTH": "20"}
        validator = Validator(config)
        with pytest.raises(KeyError):
            validator.validate()


class TestMazeGenerator:
    def test_generator_init(self) -> None:
        config = {
            "WIDTH": "20",
            "HEIGHT": "15",
            "ENTRY": "0,0",
            "EXIT": "19,14",
            "OUTPUT_FILE": "maze.txt",
            "PERFECT": "True"
        }
        generator = MazeGenerator(config)
        assert generator.width == 20
        assert generator.height == 15
        assert generator.output_file == "maze.txt"

    def test_generator_dfs(self) -> None:
        config = {
            "WIDTH": "20",
            "HEIGHT": "15",
            "ENTRY": "0,0",
            "EXIT": "19,14",
            "OUTPUT_FILE": "maze.txt",
            "PERFECT": "True",
            "ALGORITHM": "dfs"
        }
        generator = MazeGenerator(config)
        generator.generate()
        assert any(cell < 15 for row in generator.grid for cell in row)

    def test_generator_prim(self) -> None:
        config = {
            "WIDTH": "20",
            "HEIGHT": "15",
            "ENTRY": "0,0",
            "EXIT": "19,14",
            "OUTPUT_FILE": "maze.txt",
            "PERFECT": "True",
            "ALGORITHM": "prim"
        }
        generator = MazeGenerator(config)
        generator.generate()
        assert any(cell < 15 for row in generator.grid for cell in row)

    def test_generator_save(self) -> None:
        config = {
            "WIDTH": "10",
            "HEIGHT": "10",
            "ENTRY": "0,0",
            "EXIT": "9,9",
            "OUTPUT_FILE": "test_maze.txt",
            "PERFECT": "True"
        }
        generator = MazeGenerator(config)
        generator.generate()
        entry = (0, 0)
        exit_coords = (9, 9)
        generator.save(entry=entry, exit_coords=exit_coords)
        assert os.path.exists("test_maze.txt")
        with open("test_maze.txt", 'r') as f:
            lines = f.readlines()
            grid_lines = [l.strip() for l in lines if l.strip() and l.strip()[0] in '0123456789ABCDEF']
            assert len(grid_lines) == 10
            for line in grid_lines:
                for char in line:
                    assert char in '0123456789ABCDEF'
        os.unlink("test_maze.txt")

    def test_pattern_fit(self) -> None:
        config = {
            "WIDTH": "20",
            "HEIGHT": "15",
            "ENTRY": "0,0",
            "EXIT": "19,14",
            "OUTPUT_FILE": "maze.txt",
            "PERFECT": "True"
        }
        generator = MazeGenerator(config)
        assert len(generator.blocked) > 0

    def test_pattern_too_small(self) -> None:
        config = {
            "WIDTH": "5",
            "HEIGHT": "5",
            "ENTRY": "0,0",
            "EXIT": "4,4",
            "OUTPUT_FILE": "maze.txt",
            "PERFECT": "True"
        }
        generator = MazeGenerator(config)
        assert len(generator.blocked) == 0


class TestAlgorithms:
    def test_prim_algorithm(self) -> None:
        grid = [[15 for _ in range(10)] for _ in range(10)]
        algo = PrimAlgorithm()
        algo.dig_maze(grid, 10, 10, set(), False)
        assert grid[0][0] < 15
        assert any(cell < 15 for row in grid for cell in row)

    def test_dfs_algorithm(self) -> None:
        grid = [[15 for _ in range(10)] for _ in range(10)]
        algo = DFSAlgorithm()
        algo.dig_maze(grid, 10, 10, set(), False)
        assert grid[0][0] < 15
        assert any(cell < 15 for row in grid for cell in row)
