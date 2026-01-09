# domain/equipment.py

class Equipment:
    """
    Оборудование пиццерии
    """
    def __init__(self, name: str, eq_type: str, power_kw: float, cook_time_min: int = 0):
        self.name = name
        self.type = eq_type  # oven, fridge, proofing_fridge, table_fridge
        self.power_kw = power_kw
        self.cook_time_min = cook_time_min  # для печи

class EquipmentFactory:
    """
    Создаёт оборудование из JSON-конфига
    """
    @staticmethod
    def create_from_json(data: dict) -> Equipment:
        return Equipment(
            name=data.get("name", "unknown"),
            eq_type=data.get("type", "unknown"),
            power_kw=data.get("power_kw", 0.0),
            cook_time_min=data.get("cook_time_min", 10)
        )
