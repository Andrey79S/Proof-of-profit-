# engine/production.py

from domain.product import DoughBatch

class ProductionEngine:
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria

    def make_dough(self, target_amount_kg: float = 50.0, now: int = 0) -> bool:
        """
        Делает партию теста, если есть миксер и ингредиенты (мука и т.д.)
        """
        mixer = next((eq for eq in self.pizzeria.equipment.values() if eq.type == "mixer"), None)
        if not mixer:
            print("Нет миксера для замеса теста!")
            return False

        if not mixer.can_use(target_amount_kg):
            print(f"Миксер занят или партия {target_amount_kg} кг вне лимитов")
            return False

        # Предположим, что мука нужна: 0.6 кг на 1 кг теста
        flour_needed = target_amount_kg * 0.6
        flour = self.pizzeria.inventory.ingredients.get("flour")
        if not flour or flour.amount_kg < flour_needed:
            print(f"Недостаточно муки для замеса {target_amount_kg} кг теста")
            return False

        # Тратим муку
        flour.amount_kg -= flour_needed

        # Время замеса
        mix_time = mixer.mix_time_min or 20
        lifetime = self.pizzeria.equipment.get("proofing_fridge_basic", {}).get("dough_lifetime_min", 1440)

        # Энергия
        self.pizzeria.energy_consumed += mixer.power_kw * (mix_time / 60.0)
        electricity_price = self.pizzeria.economy.get("electricity_price_per_kwh", 0.12)
        self.pizzeria.expenses += mixer.power_kw * (mix_time / 60.0) * electricity_price

        # Создаём тесто
        batch = DoughBatch(amount_kg=target_amount_kg, prepared_at_min=now, expires_at_min=now + lifetime)
        self.pizzeria.inventory.add_dough_batch(batch)

        print(f"Замесили {target_amount_kg} кг теста (потрачено {flour_needed:.1f} кг муки)")
        return True
