#engine/production.py

from domain.order import Order
def make_dough(pizzeria, amount_kg: float, now: int):
    batch = DoughBatch(amount_kg, now, now + 2880)  # ← отступ!
    pizzeria.inventory.add_dough_batch(batch)
    print(f"Замешено {amount_kg} кг теста")  # ← тоже отступ!

def cook_pizza(pizzeria, order: Order):
if pizzeria.can_accept_order(order):
pizzeria.cook(order)
print(f"Приготовлена пицца: {order.recipe}")
else:д
print(f"Нельзя приготовить {order.recipe} — недостаточно ресурсов")
