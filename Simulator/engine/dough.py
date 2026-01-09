def make_dough(pizzeria, amount_kg: float, now: int):
    batch = DoughBatch(amount_kg, now, now + 2880)  # 48 часов
    pizzeria.inventory.add_dough_batch(batch)
    print(f"Замешено {amount_kg} кг теста")
