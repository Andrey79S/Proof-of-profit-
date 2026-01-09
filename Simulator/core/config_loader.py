# core/config_loader.py

import json
import os

class ConfigLoader:
    """
    Загружает все JSON-конфиги из папки
    """
    def __init__(self, config_path="config"):
        self.config_path = config_path

    def load_all(self) -> dict:
        configs = {}
        # Перечисляем нужные файлы
        filenames = ["economy.json", "recipes.json", "equipment.json", "staff.json"]
        for fname in filenames:
            path = os.path.join(self.config_path, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    key = fname.split(".")[0]  # 'economy', 'recipes', etc.
                    configs[key] = json.load(f)
            except FileNotFoundError:
                print(f"⚠️ Файл {fname} не найден, пропускаем")
                configs[fname.split(".")[0]] = {}
        return configs
