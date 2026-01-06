import json
from pathlib import Path

class Staff:
    def __init__(self, name, role, speed_multiplier=1.0):
        self.name = name
        self.role = role
        self.speed_multiplier = speed_multiplier

    def __repr__(self):
        return f"<Staff {self.name} role={self.role}>"

class StaffFactory:
    @staticmethod
    def load_all(config_folder="config/staff"):
        staff_members = {}
        folder = Path(config_folder)
        for file in folder.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                s = Staff(
                    name=data["name"],
                    role=data.get("role", "cook"),
                    speed_multiplier=data.get("speed_multiplier", 1.0)
                )
                staff_members[s.name] = s
        return staff_members
