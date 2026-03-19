import sys
from MazeGenerator.parser import Parser
from MazeGenerator.validator import Validator
from typing import Dict


def a_maze_ing() -> None:
    argc: int = len(sys.argv)

    if argc != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    filepath: str = sys.argv[1]

    try:
        parser: Parser = Parser(filepath)
        config_data: Dict[str, str] = parser.parse()

        validator: Validator = Validator(config_data)
        validator.validate()

        print("Configuration successfully loaded and validated!")
    except (FileNotFoundError, ValueError, KeyError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occured: {e}")
        sys.exit(1)


if __name__ == "__main__":
    a_maze_ing()
