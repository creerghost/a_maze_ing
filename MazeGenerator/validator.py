from typing import Dict, Set, Tuple


class Validator:
    def __init__(self, config: Dict[str, str]) -> None:
        self.config = config
        self.required_keys: Tuple[str, ...] = ("WIDTH", "HEIGHT",
                                               "ENTRY", "EXIT",
                                               "OUTPUT_FILE", "PERFECT")

    def validate(self) -> None:
        missing_keys: Set[str] = self.required_keys - self.config.keys()
        if missing_keys:
            raise KeyError(f"Missing mandatory configuration keys:"
                           f" {', '.join(missing_keys)}")
