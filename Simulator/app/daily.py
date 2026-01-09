from engine.production import ProductionEngine
from domain.order import Order

def run_daily(pizzeria):
    for _ in range(5):
        order = Order("margarita", pizzeria.clock.now())
        pizzeria.production_engine.cook(order.recipe)
        pizzeria.clock.tick(15)
