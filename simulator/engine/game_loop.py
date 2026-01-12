# engine/game_loop.py
import time
from datetime import datetime, timedelta

class GameLoop:
    """
    Авто-симуляция для всех игроков
    """
    def __init__(self, players: list, pool, tick_hours: int = 1):
        self.players = players
        self.pool = pool
        self.tick_hours = tick_hours
        self.last_tick = datetime.now()

    def tick(self):
        """
        Симулируем 1 "тик" (час)
        """
        for player in self.players:
            # Восстанавливаем энергию
            player.energy.regen()

            # Резервируем заказы из пула
            taken, pizza_orders = player.reserve.reserve_from_pool(self.pool, player.reserve.base_capacity)
            
            # Производство
            report = player.production.simulate_production(hours=self.tick_hours)
            
            # Можно начислять кристаллы бонусом (например, 1% от дохода)
            bonus_crystals = int(report["revenue"] * 0.01)
            player.crystals.add(bonus_crystals)
            
            # Отчёт
            print(f"Игрок {player} — тик {self.last_tick}")
            print(f"Резерв забрал: {taken} заказов, пиццы: {pizza_orders}")
            print(f"Производство: {report}")
            print(f"Энергия: {player.energy.get_current()}, Кристаллы: {player.crystals.get()}")
            print("-" * 50)

        # Обновляем время последнего тика
        self.last_tick += timedelta(hours=self.tick_hours)
