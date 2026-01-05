# domain/equipment.py

from enum import Enum


class EquipmentType(Enum):
    MIXER = "mixer"
    DOUGH_FRIDGE = "dough_fridge"
    INGREDIENT_FRIDGE = "ingredient_fridge"
    WORKBENCH_FRIDGE = "workbench_fridge"
    OVEN = "oven"


class Equipment:
    def __init__(
        self,
        name: str,
        eq_type: EquipmentType,
        capacity: int,
        power_kw: float,
        active_only_when_used: bool,
        params: dict
    ):
        self.name = name
        self.type = eq_type
        self.capacity = capacity              # max единиц продукта
        self.power_kw = power_kw               # кВт
        self.active_only_when_used = active_only_when_used
        self.params = params                   # спец параметры

        self.is_busy = False                   # управляется engine
        self.current_load = 0

    def can_accept(self, amount: int) -> bool:
        return self.current_load + amount <= self.capacity

    def __repr__(self):
        return f"<Equipment {self.name} ({self.type.value})>"
