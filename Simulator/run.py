from domain.order_pool import OrderPool
from domain.pizzeria import Pizzeria
from engine.simulator import SimulatorEngine, Clock

def main():
    # конфиги оборудования
    equipment_configs = {
        "oven_basic": "config/equipment/oven_basic.json",
        "mixer_basic": "config/equipment/mixer_basic.json",
        "fridge_basic": "config/equipment/fridge_basic.json",
    }

    # конфиги staff
    staff_configs = {
        "cook_junior": {"skills": {"cooking": 1}}
    }

    # рецепты
    recipes = {
        "margarita": {"ingredients": {"flour": 0.2, "tomato_sauce": 0.1, "mozzarella": 0.1}},
        "pepperoni": {"ingredients": {"flour": 0.2, "tomato_sauce": 0.1, "mozzarella": 0.1, "pepperoni": 0.1}}
    }

    # создаём пиццерию
    pizzeria = Pizzeria(equipment_configs, staff_configs, recipes)

    # пул заказов
    pool = OrderPool()
    for i in range(10):  # 10 заказов для теста
        pool.add_order("margarita", created_at=0)
        pool.add_order("pepperoni", created_at=0)

    clock = Clock()
    sim = SimulatorEngine(pizzeria, pool, clock)

    sim.run(sessions=1, hours_per_session=2)  # 1 сессия по 2 часа

if __name__ == "__main__":
    main()
