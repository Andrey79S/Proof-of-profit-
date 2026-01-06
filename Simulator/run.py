from domain.inventory import Inventory
from domain.equipment import Oven, Equipment
from domain.staff import Staff
from domain.pizzeria import Pizzeria
from domain.order_pool import OrderPool
from domain.order import Order
from core.clock import Clock
from engine.simulator import SimulatorEngine

def main():
    sessions = int(input("Сколько сессий в день: "))
    hours = int(input("Сколько часов в сессии: "))
    orders_count = int(input("Сколько заказов в пуле: "))

    # Инициализация
    inventory = Inventory()
    equipment_list = [Oven("oven_basic", power_kw=8, capacity=4, bake_time=10)]
    staff_list = [Staff("Cook 1")]
    pizzeria = Pizzeria(inventory, equipment_list, staff_list)

    order_pool = OrderPool()
    for i in range(orders_count):
        order_pool.add_order(Order(recipe="margarita", created_at=0, max_wait=60))

    clock = Clock()
    simulator = SimulatorEngine(pizzeria, order_pool, clock)
    simulator.run(sessions=sessions, hours_per_session=hours)

if __name__ == "__main__":
    main()
