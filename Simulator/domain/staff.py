import json
from dataclasses import dataclass

@dataclass
class Staff:
    name: str
    role: str
    skill_level: int = 1
    speed_modifier: float = 1.0  # >1 для ускорения

class StaffFactory:
    @staticmethod
    def create_from_json(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Staff(
            name=data.get("name"),
            role=data.get("role"),
            skill_level=data.get("skill_level", 1),
            speed_modifier=data.get("speed_modifier", 1.0)
        )
