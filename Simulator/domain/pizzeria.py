#domain/pizzeria.py

from core.config_loader import ConfigLoader
from domain.inventory import Inventory
from domain.finance import Finance
from domain.order import Order

class Pizzeria:
def init(self, loader: ConfigLoader):
self.config = {
"economy": loader.load("economy.json"),
"recipes": loader.load("recipes.json"),
}

self.inventory = Inventory()  
    self.finance = Finance()  

    self.clock = None  # будет установлен извне  

    self.add_initial_inventory()  

def add_initial_inventory(self):  
    self.inventory.add_ingredient("tomato_sauce", 50.0)  
    self.inventory.add_ingredient("mozzarella", 50.0)  
    self.inventory.add_ingredient("flour", 200.0)  
    self.inventory.add_ingredient("water", 100.0)  

    # Начальное тесто (уже готовое)  
    from domain.product import DoughBatch  
    batch = DoughBatch(30.0, prepared_at_min=-720, expires_at_min=2880)  
    self.inventory.add_dough_batch(batch)  

def can_accept_order(self, order: Order) -> bool:  
    recipe = self.config["recipes"].get(order.recipe)  
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

def cook(self, order: Order):  
    recipe = self.config["recipes"][order.recipe]  
    now = self.clock.now()  

    # Тратим  
    for ing, qty in recipe.get("ingredients", {}).items():  
        if ing != "dough":  
            self.inventory.consume_ingredient(ing, qty)  
    self.inventory.consume_dough(recipe.get("dough_kg", 0.25), now)  

    # Доход  
    self.finance.revenue += recipe.get("price", 10.0)
