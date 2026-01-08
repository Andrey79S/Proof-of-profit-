# engine/production.py

from domain.product import DoughBatch

class ProductionEngine:
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria

    def make_dough(self, now: int) -> bool:
        dough_recipe = self.pizzeria.recipes.get("dough_recipe")
        if not dough_recipe:
            print("⚠ Нет рецепта теста!")
            return False

        mixer = next((eq for eq in self.pizzeria.equipment.values() if eq.type == "mixer"), None)
        proofing_fridge = next((eq for eq in self.pizzeria.equipment.values() if eq.type == "proofing_fridge"), None)
        if not mixer or not proofing_fridge:
            print("⚠ Нет миксера или расстоечного холодильника!")
            return False

        # Текущее тесто в расстоечном холодильнике
        current_dough_kg = sum(b.amount_kg for b in self.pizzeria.inventory.dough_batches)

        # Максимум по миксеру и холодильнику
        max_by_mixer = mixer.max_batch_kg
        free_in_fridge = proofing_fridge.capacity - current_dough_kg
        target_kg = min(max_by_mixer, free_in_fridge, 20.0)  # не больше 20 кг за раз

        if target_kg < mixer.min_batch_kg:
            print(f"⚠ Нет места/нужно минимум {mixer.min_batch_kg} кг для замеса")
            return False

        # Округляем до разумного (например, по 5 кг)
        target_kg = max(mixer.min_batch_kg, round(target_kg / 5) * 5)

        # Тратим ингредиенты пропорционально
        for ing_name, per_kg in dough_recipe["ingredients_per_kg"].items():
            needed = per_kg * target_kg
            try:
                self.pizzeria.inventory.consume_ingredient(ing_name, needed)
            except ValueError:
                print(f"⚠ Недостаточно {ing_name} для {target_kg} кг теста")
                return False

        # Время замеса (базовое + на кг)
        mix_time = mixer.mix_time_min + dough_recipe.get("mix_time_per_kg_min", 0) * target_kg

        # Энергия
        self.pizzeria.energy_consumed += mixer.power_kw * (mix_time / 60.0)
        self.pizzeria.expenses += mixer.power_kw * (mix_time / 60.0) * self.pizzeria.economy.get("electricity_price_per_kwh", 0.12)

        # Партия теста
        proof_time = dough_recipe["proof_time_min"]
        lifetime = dough_recipe["lifetime_after_proof_min"]
        batch = DoughBatch(
            amount_kg=target_kg,
            prepared_at_min=now,
            expires_at_min=now + proof_time + lifetime
        )
        self.pizzeria.inventory.add_dough_batch(batch)

        print(f"✅ Замесили {target_kg} кг теста (миксер: {mixer.min_batch_kg}-{mixer.max_batch_kg} кг, холодильник: свободно {free_in_fridge:.1f} кг)")
        self.pizzeria.clock.tick(int(mix_time))  # время на замес
        return True
