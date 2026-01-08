# domain/staff.py

from dataclasses import dataclass

@dataclass
class Staff:
    name: str
    role: str
    speed_multiplier: float = 1.0
    salary_per_hour: float = 0.0

class StaffFactory:
    @staticmethod
    def create_from_json(data: dict):  # Теперь принимает dict, а не путь!
        return Staff(
            name=data.get("name"),
            role=data.get("role", "cook"),
            speed_multiplier=data.get("speed_multiplier", 1.0),
            salary_per_hour=data.get("salary_per_hour", 0.0)
        )
