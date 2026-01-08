# engine/production.py

from domain.product import DoughBatch

class ProductionEngine:
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria

    def make_dough(self, now: int) -> bool:
        """
        Замес новой партии теста.
        Требует: миксер, ингредиенты по рецепту dough_batch.json
        """
        dough_recipe = self.pizzeria.recipes.get("dough_batch")
        if not dough_recipe:
            print("⚠ Нет рецепта теста (dough_batch.json)!")
            return False

        mixer = next((eq for eq in self.pizzeria.equipment.values() if eq.type == "mixer"), None)
        if not mixer:
            print("⚠ Нет миксера!")
            return False

        batch_size = dough_recipe["batch_size_kg"]

        if not mixer.can_use(batch_size):
            print(f"⚠ Миксер занят или партия {batch_size} кг не подходит по лимитам")
            return False

        # Проверяем и тратим ингредиенты для замеса
        for ing_name, qty in dough_recipe["ingredients"].items():
            try:
                self.pizzeria.inventory.consume_ingredient(ing_name, qty)
            except ValueError as e:
                print(f"⚠ Недостаточно {ing_name} для замеса теста: {e}")
                return False

        # Время замеса
        mix_time = dough_recipe.get("mix_time_min", 20)

        # Энергия за замес
        self.pizzeria.energy_consumed += mixer.power_kw * (mix_time / 60.0)
        electricity_price = self.pizzeria.economy.get("electricity_price_per_kwh", 0.12)
        self.pizzeria.expenses += mixer.power_kw * (mix_time / 60.0) * electricity_price

        # Создаём партию теста
        # prepared_at_min — момент замеса
        # expires_at_min — через proof_time + lifetime
        proof_time = dough_recipe.get("proof_time_min", 720)   # 12 часов расстойки
        lifetime = dough_recipe.get("lifetime_min", 2880)     # 48 часов хранения после расстойки

        batch = DoughBatch(
            amount_kg=batch_size,
            prepared_at_min=now,
            expires_at_min=now + proof_time + lifetime
        )
        self.pizzeria.inventory.add_dough_batch(batch)

        print(f"✅ Замесили {batch_size} кг теста. Расстойка: {proof_time//60} ч. Готово к использованию через {proof_time//60} ч.")
        return True
