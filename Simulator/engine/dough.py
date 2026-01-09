# engine/dough.py

from domain.pizzeria import Pizzeria
from domain.product import DoughBatch

def make_dough(pizzeria: Pizzeria, amount_kg: float):
    now = pizzeria.clock.now()
    batch = DoughBatch(amount_kg, now, now + 2880)  # 48 часов
    pizzeria.inventory.add_dough_batch(batch)
    pizzeria.clock.tick(20)  # время на замес
    print(f"Замешено {amount_kg} кг теста")
