import json


class Production:
    def __init__(self):
        with open("simulator/config/ingredients.json", "r", encoding="utf-8") as f:
            self.ingredients = json.load(f)

        with open("simulator/config/recipes.json", "r", encoding="utf-8") as f:
            self.recipes = json.load(f)

    # =========================
    # БАЗОВЫЕ ФУНКЦИИ
    # =========================

    def ingredient_cost(self, ingredient: str, kg: float) -> float:
        """Стоимость ингредиента"""
        return self.ingredients[ingredient]["price_per_kg"] * kg

    # =========================
    # ТЕСТО
    # =========================

    def dough_cost(self, dough_kg: float) -> float:
        """
        Себестоимость теста по рецептуре (%)
        """
        dough_recipe = self.recipes["dough"]
        cost = 0.0

        for ingredient, ratio in dough_recipe.items():
            ingredient_kg = dough_kg * ratio
            cost += self.ingredient_cost(ingredient, ingredient_kg)

        return cost

    def dough_required_for_pizzas(self, margarita_qty: int, pepperoni_qty: int) -> float:
        """
        Сколько теста нужно для указанного количества пицц
        """
        dough_per_pizza = self.recipes["pizza_margarita"]["dough"]
        total_pizzas = margarita_qty + pepperoni_qty
        return dough_per_pizza * total_pizzas

    # =========================
    # ПИЦЦА
    # =========================

    def pizza_ingredients_cost(self, recipe_name: str) -> float:
        """
        Стоимость ингредиентов одной пиццы (БЕЗ теста)
        """
        recipe = self.recipes[recipe_name]
        cost = 0.0

        for ingredient, kg in recipe.items():
            if ingredient == "dough":
                continue
            cost += self.ingredient_cost(ingredient, kg)

        return cost

    def pizzas_cost(self, margarita_qty: int, pepperoni_qty: int) -> float:
        """
        Общая себестоимость ингредиентов всех пицц
        (тесто + начинка)
        """

        # 1. Тесто
        total_dough_kg = self.dough_required_for_pizzas(
            margarita_qty, pepperoni_qty
        )
        dough_cost = self.dough_cost(total_dough_kg)

        # 2. Начинка
        margarita_cost = (
            self.pizza_ingredients_cost("pizza_margarita") * margarita_qty
        )
        pepperoni_cost = (
            self.pizza_ingredients_cost("pizza_pepperoni") * pepperoni_qty
        )

        return dough_cost + margarita_cost + pepperoni_cost

    # =========================
    # ОТЧЁТ ДЛЯ PoP
    # =========================

    def production_report(self, margarita_qty: int, pepperoni_qty: int) -> dict:
        """
        Детальный отчёт производства для PoP-логов
        """
        total_pizzas = margarita_qty + pepperoni_qty
        dough_kg = self.dough_required_for_pizzas(
            margarita_qty, pepperoni_qty
        )

        report = {
            "pizzas": {
                "margarita": margarita_qty,
                "pepperoni": pepperoni_qty,
                "total": total_pizzas
            },
            "dough": {
                "total_kg": round(dough_kg, 3),
                "cost": round(self.dough_cost(dough_kg), 2)
            },
            "ingredients_cost": {
                "margarita": round(
                    self.pizza_ingredients_cost("pizza_margarita") * margarita_qty, 2
                ),
                "pepperoni": round(
                    self.pizza_ingredients_cost("pizza_pepperoni") * pepperoni_qty, 2
                )
            },
            "total_ingredient_cost": round(
                self.pizzas_cost(margarita_qty, pepperoni_qty), 2
            )
        }

        return report
