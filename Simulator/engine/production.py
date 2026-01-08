# engine/production.py

from domain.product import DoughBatch

class ProductionEngine:
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria

    def make_dough(self, amount_kg: float, now: int) -> bool:
        mixer = next((eq for eq in self.pizzeria.equipment.values() if eq.type == "mixer"), None)
        if not mixer or not mixer.can_use(amount_kg):
            return False

        # Время замеса берём из оборудования
        mix_time = mixer.mix_time_min or 15  # fallback
        lifetime = mixer.dough_lifetime_min or 1440

        # Энергия за замес
        self.pizzeria.energy_consumed += mixer.power_kw * (mix_time / 60.0)
        self.pizzeria.expenses += self.pizzeria.energy_consumed * self.pizzeria.economy.get("electricity_price_per_kwh", 0.12)

        # Создаём тесто
        batch = DoughBatch(amount_kg, now, now + lifetime)
        self.pizzeria.inventory.add_dough_batch(batch)
        return True
