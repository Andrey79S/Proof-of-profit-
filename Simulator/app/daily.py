# app/daily.py

from engine.production import ProductionEngine
from engine.energy import EnergyEngine
from engine.spoilage import SpoilageEngine

class DailySimulator:
    """
    Симуляция рабочего дня пиццерии
    """
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria
        self.production_engine = ProductionEngine(pizzeria)
        self.energy_engine = EnergyEngine(pizzeria)
        self.spoilage_engine = SpoilageEngine(pizzeria)

    def run_day(self, orders: list, day_minutes: int = 480):
        """
        Симулируем рабочий день.
        orders: список заказов
        day_minutes: длительность рабочего дня в минутах (например, 8 часов = 480)
        """
        now = self.pizzeria.clock.now() if self.pizzeria.clock else 0
        end_time = now + day_minutes

        for order in orders:
            if self.pizzeria.clock and self.pizzeria.clock.now() >= end_time:
                break  # день закончился

            if not self.pizzeria.can_accept_order(order):
                continue  # пропускаем заказ

            # Готовим заказ через ProductionEngine
            cook_time = self.production_engine.cook_order(order)

            # Сдвигаем часы на время готовки
            if self.pizzeria.clock:
                self.pizzeria.clock.tick(cook_time)

        # --- Энергопотребление холодильников за день ---
        self.energy_engine.daily_fridge_consumption()

        # --- Порча ингредиентов и теста ---
        self.spoilage_engine.spoil_ingredients()

        # --- Финансовая сводка ---
        summary = {
            "revenue": self.pizzeria.revenue,
            "expenses": self.pizzeria.expenses,
            "losses": self.pizzeria.losses,
            "energy_consumed_kwh": self.pizzeria.energy_consumed
        }

        return summary
