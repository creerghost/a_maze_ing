import os
from typing import Dict


class Parser:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def parse(self) -> Dict[str, str]:
        config: Dict[str, str] = {}

        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"The file '{self.filepath}'"
                                    f" was not found")

        with open(self.filepath, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if '=' not in line:
                    raise ValueError(f"Bad syntax on line"
                                     f" {line_num}: '{line}'")
                k, v = line.split('=', 1)
                config[k.strip()] = v.strip()
        return config
