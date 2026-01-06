from domain.inventory import Inventory
from domain.equipment import Oven
from domain.staff import Staff
from domain.pizzeria import Pizzeria
from domain.order_pool import OrderPool
from domain.order import Order
from core.clock import Clock
from engine.simulator import SimulatorEngine

def main():
    sessions = int(input("Сессий: "))
    hours = int(input("Часов в сессии: "))
    pool_size = int(input("Заказов в пуле: "))

    inventory = Inventory()
    oven = Oven("oven_basic", 8, 4, 10)
    staff = [Staff("Cook")]

    pizzeria = Pizzeria(inventory, [oven], staff)

    pool = OrderPool()
    for _ in range(pool_size):
        pool.add_order(Order("margarita", 0, 120))

    clock = Clock()
    sim = SimulatorEngine(pizzeria, pool, clock)
    sim.run(sessions, hours)

if __name__ == "__main__":
    main()
