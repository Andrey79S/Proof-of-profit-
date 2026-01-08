# core/config_loader.py

import json
from pathlib import Path


class ConfigLoader:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def load_folder(self, relative_path: str) -> dict:
        folder = self.base_path / relative_path
        result = {}

        for file in folder.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # id берём либо из файла, либо из поля id
            item_id = data.get("id") or file.stem
            result[item_id] = data

        return result

    def load_all(self) -> dict:
        return {
            "equipment": self.load_folder("equipment"),
            "recipes": self.load_folder("recipes"),
            "staff": self.load_folder("staff"),
        }
