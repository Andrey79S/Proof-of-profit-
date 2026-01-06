from core.clock import Clock
from core.scheduler import Scheduler
from domain.pizzeria import Pizzeria
from domain.order_pool import OrderPool
from domain.equipment import EquipmentFactory
from domain.staff import Staff
from engine.simulator import SimulatorEngine
from engine.procurement import Procurement
import random

def main():
    print("=== Симулятор PoP пиццерии ===")

    # 1️⃣ Настройки симуляции
    sessions = int(input("Количество сессий: "))
    hours_per_session = int(input("Сколько часов в сессии: "))
    orders_in_pool = int(input("Сколько заказов в общем пуле: "))

    # 2️⃣ Создаём часы и планировщик
    clock = Clock()
    scheduler = Scheduler(clock)

    # 3️⃣ Создаём оборудование через фабрику
    equipment_factory = EquipmentFactory(folder="config/equipment")
    equipment = equipment_factory.create_all()  # словарь с объектами оборудования

    # 4️⃣ Создаём персонал
    staff = [Staff(name="Cook Junior", skill_level=1)]

    # 5️⃣ Создаём пиццерию
    pizzeria = Pizzeria(equipment=equipment, staff=staff)

    # 6️⃣ Создаём общий пул заказов
    order_pool = OrderPool()
    recipes = ["margarita", "pepperoni"]
    for _ in range(orders_in_pool):
        recipe = random.choice(recipes)
        max_wait = random.randint(30, 90)  # время ожидания заказа в минутах
        order_pool.add_order(recipe=recipe, created_at=clock.now(), max_wait=max_wait)

    # 7️⃣ Создаём модуль закупок
    procurement = Procurement()
    procurement.auto_restock(pizzeria.table_fridge)  # первичное пополнение

    # 8️⃣ Создаём движок симуляции
    simulator = SimulatorEngine(pizzeria, order_pool, clock)

    # 9️⃣ Запускаем симуляцию
    simulator.run(sessions=sessions, hours_per_session=hours_per_session)

    print("\n=== Симуляция завершена ===")

if __name__ == "__main__":
    main()
