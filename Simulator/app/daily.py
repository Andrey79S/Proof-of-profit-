# app/daily.py

from engine.production import cook_pizza
from domain.order import Order

def run_daily(pizzeria):
    print("Рабочий день начался")
    for _ in range(5):  # 5 пицц в день (пример)
        order = Order("margarita", pizzeria.clock.now())
        cook_pizza(pizzeria, order)
