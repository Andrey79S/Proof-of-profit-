from domain.inventory import Inventory
from domain.finance import Finance
from domain.equipment import Equipment
from domain.staff import Staff
from engine.production import ProductionEngine

class Pizzeria:
    def __init__(self, loader):
        self.config = {
            "economy": loader.load("economy.json"),
            "recipes": loader.load_dir("recipes"),
            "equipment": loader.load_dir("equipment"),
            "staff": loader.load_dir("staff"),
        }

        self.inventory = Inventory()
        self.finance = Finance()
        self.production_engine = ProductionEngine(self)

        self.clock = None

        self._load_entities()

    def _load_entities(self):
        for data in self.config["equipment"].values():
            self.equipment.append(Equipment(data))
        for data in self.config["staff"].values():
            self.staff.append(Staff(data))

    def can_accept_order(self, recipe: str) -> bool:
        r = self.config["recipes"].get(recipe)
        if not r:
            return False

        now = self.clock.now()

        for ing, qty in r.get("ingredients", {}).items():
            if ing != "dough" and self.inventory.ingredients.get(ing, 0.0) < qty:
                return False

        dough_needed = r.get("dough_kg", 0.25)
        available = sum(b.amount_kg for b in self.inventory.dough_batches if not b.is_expired(now))
        return available >= dough_needed

    def cook(self, recipe: str):
        r = self.config["recipes"][recipe]
        now = self.clock.now()

        for ing, qty in r.get("ingredients", {}).items():
            if ing != "dough":
                self.inventory.consume_ingredient(ing, qty)
        self.inventory.consume_dough(r.get("dough_kg", 0.25), now)

        self.finance.add_revenue(r["price"])
