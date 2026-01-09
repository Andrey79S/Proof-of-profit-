from domain.inventory import Inventory
from domain.equipment import Equipment
from domain.staff import Staff

class Finance:
    def __init__(self):
        self.revenue = 0.0
        self.expenses = 0.0
        self.losses = 0.0

class Pizzeria:
    def __init__(self, loader):
        self.config = {
            "economy": loader.load("economy.json"),
            "recipes": loader.load("recipes.json"),
            "equipment": loader.load("equipment.json"),
            "staff": loader.load("staff.json"),
        }

        self.inventory = Inventory()
        self.finance = Finance()

        self.equipment = []  # список Equipment
        self.staff = []      # список Staff

        self.clock = None

    def can_accept_order(self, order_recipe: str) -> bool:
        recipe = self.config["recipes"].get(order_recipe)
        if not recipe:
            return False

        for ing, qty in recipe.get("ingredients", {}).items():
            if ing != "dough" and self.inventory.ingredients.get(ing, 0.0) < qty:
                return False

        dough_needed = recipe.get("dough_kg", 0.25)
        available = sum(b.amount_kg for b in self.inventory.dough_batches if not b.is_expired(self.clock.now()))
        return available >= dough_needed

    def cook(self, order_recipe: str):
        recipe = self.config["recipes"][order_recipe]
        for ing, qty in recipe.get("ingredients", {}).items():
            if ing != "dough":
                self.inventory.consume_ingredient(ing, qty)
        self.inventory.consume_dough(recipe.get("dough_kg", 0.25), self.clock.now())

        self.finance["revenue"] += recipe["price"]
