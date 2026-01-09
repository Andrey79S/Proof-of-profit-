def apply_spoilage(pizzeria, now: int):
    spoiled = 0.0
    pizzeria.inventory.dough_batches = [b for b in pizzeria.inventory.dough_batches if not b.is_expired(now)]
    # Простая модель порчи ингредиентов
    for name, amount in list(pizzeria.inventory.ingredients.items()):
        if amount > 0 and random.random() < 0.01:  # 1% шанс в день
            loss = amount * 0.1
            pizzeria.inventory.ingredients[name] -= loss
            spoiled += loss
    pizzeria.finance["losses"] += spoiled * 2.0  # стоимость
