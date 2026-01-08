import json
from pathlib import Path

class ConfigLoader:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def load_all(self):
        configs = {
            "economy": self._load_json(self.base_path / "economy.json"),
            "recipes": self._load_dir(self.base_path / "recipes"),
            "equipment": self._load_dir(self.base_path / "equipment"),
            "staff": self._load_dir(self.base_path / "staff"),
        }
        return configs

    def _load_json(self, path: Path):
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _load_dir(self, dir_path: Path):
        if not dir_path.exists() or not dir_path.is_dir():
            return {}
        items = {}
        for file in dir_path.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                name = data.get("name")
                if not name:
                    print(f"Предупреждение: JSON без 'name' пропущен: {file}")
                    continue
                items[name] = data
            except Exception as e:
                print(f"Ошибка загрузки {file}: {e}")
        return items
