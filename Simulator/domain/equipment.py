from domain.equipment import EquipmentFactory
from domain.staff import StaffFactory
import json
from pathlib import Path

class Pizzeria:
    def __init__(self, config_folder="config"):
        # оборудование
        self.equipment = EquipmentFactory.load_all(f"{config_folder}/equipment")
        # персонал
        self.staff = StaffFactory.load_all(f"{config_folder}/staff")
        # экономика
        with open(Path(config_folder) / "economy.json", "r", encoding="utf-8") as f:
            self.economy = json.load(f)

        print(f"Loaded {len(self.equipment)} equipment")
        print(f"Loaded {len(self.staff)} staff")
        print(f"Economy keys: {list(self.economy.keys())}")
