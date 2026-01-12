# game/currencies/energy.py

class Energy:
    """
    Энергия игрока:
    - current: текущее количество
    - max_energy: максимум
    - regen_per_tick: восстановление (например, 1 энергия/час)
    """

    def __init__(self, max_energy: int = 10, regen_per_tick: int = 1):
        self.max_energy = max_energy
        self.current = max_energy
        self.regen_per_tick = regen_per_tick

    def use(self, amount: int) -> bool:
        if amount <= 0:
            return True
        if self.current < amount:
            return False  # недостаточно энергии
        self.current -= amount
        return True

    def regen(self):
        self.current = min(self.max_energy, self.current + self.regen_per_tick)

    def get_current(self) -> int:
        return self.current
