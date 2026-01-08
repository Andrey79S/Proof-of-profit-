from domain.product import DoughBatch

class ProductionEngine:
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria

    def make_dough(self, now: int) -> bool:
        recipe = self.pizzeria.recipes.get("dough_recipe")
        if not recipe:
            return False

        mixer = next((eq for eq in self.pizzeria.equipment.values() if eq.type == "mixer"), None)
        fridge = next((eq for eq in self.pizzeria.equipment.values() if eq.type == "proofing_fridge"), None)
        if not mixer or not fridge:
            return False

        current_dough = sum(b.amount_kg for b in self.pizzeria.inventory.dough_batches)
        free_space = fridge.capacity - current_dough
        target_kg = min(mixer.max_batch_kg, free_space)
        target_kg = max(mixer.min_batch_kg, target_kg)

        if target_kg < mixer.min_batch_kg:
            return False

        # Тратим ингредиенты
        for ing, per_kg in recipe["ingredients_per_kg"].items():
            needed = per_kg * target_kg
            try:
                self.pizzeria.inventory.consume_ingredient(ing, needed)
            except:
                return False

        mix_time = recipe["mix_time_min"]
        self.pizzeria.energy_consumed += mixer.power_kw * (mix_time / 60)
        self.pizzeria.expenses += mixer.power_kw * (mix_time / 60) * 0.12

        batch = DoughBatch(target_kg, now, now + recipe["proof_time_min"] + recipe["lifetime_min"])
        self.pizzeria.inventory.add_dough_batch(batch)
        print(f"Замесили {target_kg:.1f} кг теста")
        return True
