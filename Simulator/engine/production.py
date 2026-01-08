from domain.pizzeria import Pizzeria
from domain.product import DoughBatch

class ProductionEngine:
    def __init__(self, pizzeria: Pizzeria):
        self.pizzeria = pizzeria

    def make_dough(self, amount_kg: float, now: int):
        mixer = self.pizzeria.equipment.get("mixer_basic")
        if not mixer or not mixer.can_use(amount_kg):
            return False
        mix_time = mixer.mix_time_min  # Из config, но в JSON mix_time_min
        # Симулировать время
        lifetime = self.pizzeria.equipment["proofing_fridge_basic"].dough_lifetime_min
        batch = DoughBatch(amount_kg, now, now + lifetime)
        self.pizzeria.inventory.add_dough_batch(batch)
        return True
