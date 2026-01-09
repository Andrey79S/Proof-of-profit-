# app/offline.py

from engine.spoilage import SpoilageEngine
from engine.energy import EnergyEngine

class OfflineProcessor:
    """
    Обрабатывает все события пиццерии за период оффлайн
    """
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria
        self.spoilage_engine = SpoilageEngine(pizzeria)
        self.energy_engine = EnergyEngine(pizzeria)

    def apply_offline(self, offline_minutes: int):
        """
        Применяем все эффекты за время оффлайн
        """
        # Сдвигаем часы
        if self.pizzeria.clock:
            self.pizzeria.clock.tick(offline_minutes)

        # Порча ингредиентов и теста
        self.spoilage_engine.spoil_ingredients()

        # Энергопотребление холодильников
        # Считаем пропорционально offline_minutes
        fridge_power = sum(
            eq.power_kw for eq in self.pizzeria.equipment.values()
            if eq.type in ["fridge", "proofing_fridge", "table_fridge"]
        )
        hours = offline_minutes / 60.0
        energy = fridge_power * hours
        self.pizzeria.energy_consumed += energy
        self.pizzeria.expenses += energy * self.pizzeria.economy.get("electricity_price_per_kwh", 0.12)
