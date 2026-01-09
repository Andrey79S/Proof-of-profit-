import random

def apply_spoilage(pizzeria, now: int):
    spoiled = 0.0
    pizzeria.inventory.dough_batches = [b for b in pizzeria.inventory.dough_batches if not b.is_expired(now)]
    for name, amount in list(pizzeria.inventory.ingredients.items()):
        if random.random() < 0.02:
            loss = amount * 0.1
            pizzeria.inventory.ingredients[name] -= loss
            spoiled += loss
    pizzeria.finance.add_loss(spoiled * 2.0)
