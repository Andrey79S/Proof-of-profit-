from core.config_loader import ConfigLoader
from domain.order_pool import OrderPool
from domain.pizzeria import Pizzeria
from domain.order import Order
from core.clock import Clock
from engine.simulator import SimulatorEngine

def main():
    # 1️⃣ Загружаем конфиги
    loader = ConfigLoader("config")
    configs = loader.load_all()

    equipment_configs = configs["equipment"]
    recipe_configs = configs["recipes"]
    staff_configs = configs["staff"]

    # 2️⃣ Создаём Pizzeria (игровая пиццерия)
    pizzeria = Pizzeria(
        equipment_configs=equipment_configs,
        recipe_configs=recipe_configs,
        staff_configs=staff_configs
    )

    # 3️⃣ Создаём пул заказов (ручной ввод для симуляции)
    pool = OrderPool()
    num_orders = int(input("Сколько заказов в пуле сегодня: "))
    for i in range(num_orders):
        # случайно выбираем рецепт
        recipe = list(recipe_configs.keys())[i % len(recipe_configs)]
        # создаём заказ (max_wait=30 минут)
        pool.add_order(Order(recipe=recipe, created_at=0, max_wait=30))

    # 4️⃣ Создаём часы для симуляции
    clock = Clock()

    # 5️⃣ Создаём движок симуляции
    engine = SimulatorEngine(pizzeria, pool, clock)

    # 6️⃣ Задаём параметры симуляции
    sessions = int(input("Сколько рабочих сессий в день: "))
    hours_per_session = int(input("Сколько часов в каждой сессии: "))

    # 7️⃣ Запуск симуляции
    engine.run(sessions, hours_per_session)

if __name__ == "__main__":
    main()
