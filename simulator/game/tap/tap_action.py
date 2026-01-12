# game/tap/tap_action.py
from typing import Optional

class TapAction:
    """
    Один тап игрока:
    - проверка энергии
    - добавление заказов в пул
    - расход кристаллов или бонусы
    """
    def __init__(self, player, pool):
        self.player = player
        self.pool = pool

    def tap(self, multiplier: Optional[int] = 1):
        # Проверяем энергию
        if self.player.energy.current <= 0:
            return 0  # тап не сработал

        self.player.energy.use(1)  # стандартная стоимость энергии

        # Рассчитываем количество заказов
        base = multiplier * self.player.tap_upgrades.amount_level
        self.pool.add_orders(base)
        return base
