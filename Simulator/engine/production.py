# engine/production.py

from domain.pizzeria import Pizzeria
from domain.order import Order

def cook_pizza(pizzeria: Pizzeria, order: Order):
    if pizzeria.can_accept_order(order.recipe):
        pizzeria.cook(order.recipe)
        pizzeria.clock.tick(15)  # пример: 15 мин на пиццу
    else:
        print(f"Заказ {order.recipe} отклонён — недостаточно ресурсов")
