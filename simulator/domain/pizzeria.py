from domain.menu import Menu

class Pizzeria:
    def __init__(self, base_capacity_per_hour, reserve, ledger):
        self.base_capacity_per_hour = base_capacity_per_hour
        self.reserve = reserve
        self.ledger = ledger

        # апгрейды
        self.tap_level = 1
        self.reserve_level = 1
        self.capacity_level = 1
        self.efficiency_level = 1
        self.equipment_level = 1
        self.staff_level = 1

        # меню
        self.menu = Menu()

    # ===== коэффициенты апгрейдов =====
    def tap_power(self) -> int:
        return int(1 * (1.2 ** (self.tap_level - 1)) * (1 + 0.1*(self.staff_level-1)))

    def max_reserve(self) -> int:
        return int(100 * (1.5 ** (self.reserve_level - 1)) * (1 + 0.1*(self.equipment_level-1)))

    def production_capacity(self, hours: float) -> int:
        capacity = self.base_capacity_per_hour * (1.3 ** (self.capacity_level - 1))
        capacity *= (1 + 0.1*(self.staff_level-1))
        capacity *= (1 + 0.05*(self.equipment_level-1))
        return int(capacity * hours)

    def cost_multiplier(self) -> float:
        return max(0.5, 1.0 - 0.05 * (self.efficiency_level - 1))
