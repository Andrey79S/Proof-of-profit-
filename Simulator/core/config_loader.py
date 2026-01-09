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

    def load_dir(self, dir_name: str) -> dict:
        dir_path = self.base_path / dir_name
        items = {}
        if dir_path.is_dir():
            for file in dir_path.glob("*.json"):
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                name = data.get("name") or file.stem
                items[name] = data
        return items
