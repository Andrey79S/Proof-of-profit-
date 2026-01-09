# domain/pizzeria.py

from core.config_loader import ConfigLoader
from domain.inventory import Inventory
from domain.finance import Finance
from domain.product import DoughBatch

class Pizzeria:
    def __init__(self, loader: ConfigLoader):
        self.config = {
            "economy": loader.load("economy.json"),
            "recipes": loader.load("recipes.json"),
            "equipment": loader.load("equipment.json"),
            "staff": loader.load("staff.json"),
        }

        self.inventory = Inventory()
        self.finance = Finance()

        self.clock = None  # будет установлен

        self._add_initial_inventory()

    def _add_initial_inventory(self):
        """Начальный запас для тестов"""
        self.inventory.add_ingredient("tomato_sauce", 50.0)
        self.inventory.add_ingredient("mozzarella", 50.0)
        self.inventory.add_ingredient("flour", 200.0)
        self.inventory.add_ingredient("water", 100.0)
        self.inventory.add_ingredient("salt", 5.0)
        self.inventory.add_ingredient("yeast", 2.0)

        # Начальная партия теста (уже готового)
        initial_batch = DoughBatch(amount_kg=20.0, prepared_at_min=-720, expires_at_min=2880)
        self.inventory.add_dough_batch(initial_batch)

    def can_accept_order(self, order_recipe: str) -> bool:
        recipe = self.config["recipes"].get(order_recipe)
        if not recipe:
            return False

        now = self.clock.now()

        # Ингредиенты
        for ing, qty in recipe.get("ingredients", {}).items():
            if ing != "dough" and self.inventory.ingredients.get(ing, 0.0) < qty:
                return False

        # Тесто
        dough_needed = recipe.get("dough_kg", 0.25)
        available = sum(b.amount_kg for b in self.inventory.dough_batches if not b.is_expired(now))
        return available >= dough_needed

    def cook(self, order_recipe: str):
        recipe = self.config["recipes"][order_recipe]
        now = self.clock.now()

        # Списание
        for ing, qty in recipe.get("ingredients", {}).items():
            if ing != "dough":
                self.inventory.consume_ingredient(ing, qty)
        self.inventory.consume_dough(recipe.get("dough_kg", 0.25), now)

        # Доход
        price = recipe.get("price", 10.0)
        self.finance.add_revenue(price)

        print(f"Приготовлена {order_recipe} за {price}$")
