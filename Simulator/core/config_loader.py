import json
from pathlib import Path

class ConfigLoader:
    def __init__(self, base_path: str = "config"):
        self.base_path = Path(base_path)

    def load(self, filename: str) -> dict:
        path = self.base_path / filename
        if not path.exists():
            raise FileNotFoundError(f"Конфиг не найден: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
