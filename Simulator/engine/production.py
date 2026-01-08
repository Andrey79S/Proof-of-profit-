from domain.product import DoughBatch

class ProductionEngine:
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria

    def make_dough(self, now: int) -> bool:
        dough_recipe = self.pizzeria.recipes.get("dough_batch")
        if not dough_recipe:
            print("Нет рецепта для теста!")
            return False

        mixer = next((eq for eq in self.pizzeria.equipment.values() if eq.type == "mixer"), None)
        if not mixer or not mixer.can_use(dough_recipe["batch_size_kg"]):
            print("Миксер недоступен")
            return False

        # Тратим ингредиенты для замеса
        for ing_name, qty in dough_recipe["ingredients"].items():
            try:
                self.pizzeria.inventory.consume_ingredient(ing_name, qty)
            except ValueError:
                print(f"Недостаточно {ing_name} для замеса")
                return False

        mix_time = dough_recipe["mix_time_min"]
        proof_time = dough_recipe["proof_time_min"]
        lifetime = dough_recipe["lifetime_min"]

        # Энергия
        self.pizzeria.energy_consumed += mixer.power_kw * (mix_time / 60.0)
        self.pizzeria.expenses += mixer.power_kw * (mix_time / 60.0) * self.pizzeria.economy.get("electricity_price_per_kwh", 0.12)

        # Создаём партию теста (prepared_at = now, готово после proof_time)
        batch = DoughBatch(amount_kg=dough_recipe["batch_size_kg"], prepared_at_min=now, expires_at_min=now + proof_time + lifetime)
        self.pizzeria.inventory.add_dough_batch(batch)

        print(f"Замесили {dough_recipe['batch_size_kg']} кг теста. Расстойка 12 ч, срок хранения 48 ч.")
        return True
