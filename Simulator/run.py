from domain.pizzeria import Pizzeria
from domain.order import Order
from domain.order_pool import OrderPool
from core.clock import Clock
from engine.simulator import SimulatorEngine
import os

def load_files(folder):
    """Возвращает словарь {имя_файла_без_расширения: полный_путь}"""
    files = {}
    for f in os.listdir(folder):
        if f.endswith(".json"):
            key = f.replace(".json", "")
            files[key] = os.path.join(folder, f)
    return files

def main():
    # Конфиги
    equipment_files = load_files("config/equipment")
    staff_files = load_files("config/staff")
    recipe_files = load_files("config/recipes")

    # Создаём пиццерию
    pizzeria = Pizzeria(equipment_files, staff_files, recipe_files)

    # Создаём пул заказов (для симуляции укажем вручную)
    order_pool = OrderPool()
    order_pool.add_order(Order("margarita", created_at=0, max_wait=60))
    order_pool.add_order(Order("pepperoni", created_at=0, max_wait=60))

    # Часы симуляции
    clock = Clock()

    # Симулятор
    simulator = SimulatorEngine(pizzeria, order_pool, clock)

    # Сессии: 1 день = 8 часов (для примера)
    sessions = 1
    hours_per_session = 8

    simulator.run(sessions, hours_per_session)

if __name__ == "__main__":
    main()
