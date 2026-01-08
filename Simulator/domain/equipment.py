# domain/equipment.py

class Equipment:
    def __init__(
        self,
        name: str,
        type: str,
        capacity: float = 0.0,          # унифицировано: кг для холодильников, пицц для печей
        power_kw: float = 0.0,
        cook_time_min: int = None,
        mix_time_min: int = None,
        min_batch_kg: float = 0.0,
        max_batch_kg: float = 0.0,
        dough_lifetime_min: int = None,
        ingredient_lifetime_min: int = None,
        opened_ingredient_lifetime_min: int = None,
    ):
        self.name = name
        self.type = type
        self.capacity = capacity
        self.power_kw = power_kw
        self.cook_time_min = cook_time_min
        self.mix_time_min = mix_time_min
        self.min_batch_kg = min_batch_kg
        self.max_batch_kg = max_batch_kg
        self.dough_lifetime_min = dough_lifetime_min
        self.ingredient_lifetime_min = ingredient_lifetime_min
        self.opened_ingredient_lifetime_min = opened_ingredient_lifetime_min
        self.is_busy = False

    def can_use(self, amount_kg: float = 0.0) -> bool:
        if self.type == "mixer":
            return self.min_batch_kg <= amount_kg <= self.max_batch_kg and not self.is_busy
        return not self.is_busy


class EquipmentFactory:
    @staticmethod
    def create_from_json(data: dict):
        return Equipment(
            name=data["name"],
            type=data.get("type", ""),
            capacity=data.get("capacity", data.get("capacity_kg", 0)),
            power_kw=data.get("power_kw", 0.0),
            cook_time_min=data.get("cook_time_min"),
            mix_time_min=data.get("mix_time_min"),
            min_batch_kg=data.get("min_batch_kg", 0),
            max_batch_kg=data.get("max_batch_kg", 0),
            dough_lifetime_min=data.get("dough_lifetime_min"),
            ingredient_lifetime_min=data.get("ingredient_lifetime_min"),
            opened_ingredient_lifetime_min=data.get("opened_ingredient_lifetime_min"),
        )
