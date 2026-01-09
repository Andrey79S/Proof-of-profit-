# engine/spoilage.py

import random

def apply_spoilage(pizzeria, now: int):
    spoiled = 0.0

    # Порча теста
    pizzeria.inventory.dough_batches = [b for b in pizzeria.inventory.dough_batches if not b.is_expired(now)]

    # Порча ингредиентов (простая модель)
    for name, amount in list(pizzeria.inventory.ingredients.items()):
        if amount > 0 and random.random() < 0.02:  # 2% шанс в день
            loss = amount * 0.1
            pizzeria.inventory.ingredients[name] -= loss
            spoiled += loss

    pizzeria.finance.add_loss(spoiled * 2.0)  # стоимость
    if spoiled > 0:
        print(f"Порча: {spoiled:.2f} кг, потери {spoiled * 2.0:.2f}$")
