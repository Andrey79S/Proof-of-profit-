#engine/production.py

from domain.order import Order

def cook_pizza(pizzeria, order: Order):
if pizzeria.can_accept_order(order):
pizzeria.cook(order)
print(f"Приготовлена пицца: {order.recipe}")
else:д
print(f"Нельзя приготовить {order.recipe} — недостаточно ресурсов")
