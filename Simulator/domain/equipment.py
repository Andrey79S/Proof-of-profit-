# domain/equipment.py

from enum import Enum


class EquipmentType(Enum):
    OVEN = "oven"
    MIXER = "mixer"
    FRIDGE = "fridge"
    PROOF_FRIDGE = "proof_fridge"
    TABLE_FRIDGE = "table_fridge"


class Equipment:
    def __init__(
        self,
        name: str,
        eq_type: EquipmentType,
        power_kw: float,
        capacity: int = 0,
        auto_off_when_empty: bool = False
    ):
        self.name = name
        self.type = eq_type

        # Энергия
        self.power_kw = power_kw
        self.enabled = False
        self.auto_off_when_empty = auto_off_when_empty

        # Вместимость / занятость
        self.capacity = capacity
        self.used_capacity = 0
        self.busy = False

    # -------------------------
    # Состояния
    # -------------------------

    def turn_on(self):
        self.enabled = True

    def turn_off(self):
        self.enabled = False
        self.busy = False

    def is_available(self) -> bool:
        return self.enabled and not self.busy

    def has_free_capacity(self, amount: int = 1) -> bool:
        if self.capacity == 0:
            return True
        return self.used_capacity + amount <= self.capacity

    # -------------------------
    # Работа с вместимостью
    # -------------------------

    def occupy(self, amount: int = 1):
        if not self.has_free_capacity(amount):
            raise RuntimeError(f"{self.name}: нет свободного места")

        self.used_capacity += amount
        self.busy = True

    def release(self, amount: int = 1):
        self.used_capacity = max(0, self.used_capacity - amount)

        if self.used_capacity == 0:
            self.busy = False

            if self.auto_off_when_empty:
                self.turn_off()

    # -------------------------
    # Диагностика
    # -------------------------

    def __repr__(self):
        return (
            f"<Equipment {self.name} "
            f"type={self.type.value} "
            f"enabled={self.enabled} "
            f"busy={self.busy} "
            f"capacity={self.used_capacity}/{self.capacity}>"
    )
