class Production:
    def __init__(self, config: dict):
        self.ingredients = config["ingredients"]
        self.recipes = config["recipes"]
        self.prices = config["prices"]
        self.equipment = config["equipment"]

        # Остатки
        self.dough_kg = 0.0

        # Статистика
        self.total_energy_kwh = 0.0

    # ---------- ВСПОМОГАТЕЛЬНОЕ ----------

    def _ingredient_cost(self, name, kg):
        return self.ingredients[name]["price_per_kg"] * kg

    # ---------- ТЕСТО ----------

    def mix_dough(self):
        mixer = self.equipment["dough_mixer"]

        batch_kg = mixer["min_load"]
        recipe = self.recipes["dough"]

        cost = 0.0
        for ingredient, part in recipe.items():
            cost += self._ingredient_cost(ingredient, part * batch_kg)

        # энергия
        energy = (
            mixer["power_kw"] *
            mixer["time_min"] / 60
        )

        self.dough_kg += batch_kg
        self.total_energy_kwh += energy

        return {
            "kg": batch_kg,
            "cost": cost,
            "energy_kwh": energy
        }

    # ---------- ПИЦЦА ----------

    def make_pizza(self, pizza_type):
        recipe_key = f"pizza_{pizza_type.lower()}"
        recipe = self.recipes[recipe_key]

        dough_needed = recipe["dough"]

        # если теста не хватает — мешаем
        if self.dough_kg < dough_needed:
            self.mix_dough()

        if self.dough_kg < dough_needed:
            return {"success": False}

        self.dough_kg -= dough_needed

        ingredient_cost = 0.0
        for ingredient, kg in recipe.items():
            if ingredient == "dough":
                continue
            ingredient_cost += self._ingredient_cost(ingredient, kg)

        # печь
        oven = self.equipment["oven"]
        energy = oven["power_kw"] / oven["capacity"]

        self.total_energy_kwh += energy

        price = self.prices["pizza_prices"][pizza_type]

        return {
            "success": True,
            "ingredient_cost": ingredient_cost,
            "energy_kwh": energy,
            "price": price
        }
