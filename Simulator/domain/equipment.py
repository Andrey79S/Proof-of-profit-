import json
from pathlib import Path

class Equipment:
    def __init__(self, name, type_, power_kw=0, **kwargs):
        self.name = name
        self.type = type_
        self.power_kw = power_kw
        self.params = kwargs

    def __repr__(self):
        return f"<Equipment {self.name} type={self.type}>"

class EquipmentFactory:
    @staticmethod
    def load_all(config_folder="config/equipment"):
        equipments = {}
        folder = Path(config_folder)
        for file in folder.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                eq = Equipment(
                    name=data["name"],
                    type_=data.get("type"),
                    power_kw=data.get("power_kw", 0),
                    **{k: v for k, v in data.items() if k not in ["name", "type", "power_kw"]}
                )
                equipments[eq.name] = eq
        return equipments
