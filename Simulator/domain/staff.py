# domain/staff.py

class Staff:
    """
    Персонал пиццерии
    """
    def __init__(self, name: str, role: str, speed_multiplier: float = 1.0):
        self.name = name
        self.role = role  # cook, cashier, cleaner и т.д.
        self.speed_multiplier = speed_multiplier  # влияет на скорость готовки

class StaffFactory:
    """
    Создаёт персонал из JSON-конфига
    """
    @staticmethod
    def create_from_json(data: dict) -> Staff:
        return Staff(
            name=data.get("name", "unknown"),
            role=data.get("role", "cook"),
            speed_multiplier=data.get("speed_multiplier", 1.0)
        )
