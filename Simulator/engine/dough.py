from domain.pizzeria import Pizzeria
from domain.product import DoughBatch

def make_dough(pizzeria: Pizzeria, amount_kg: float):
    now = pizzeria.clock.now()
    batch = DoughBatch(amount_kg, now, now + 2880)
    pizzeria.inventory.add_dough_batch(batch)
