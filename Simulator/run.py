from domain.pizzeria import Pizzeria
from domain.order_pool import OrderPool
from core.clock import Clock
from core.scheduler import Scheduler
from engine.simulator import SimulatorEngine

# Инициализация
pizzeria = Pizzeria(config_path="config")
pizzeria.add_initial_inventory()

order_pool = OrderPool()
pizzeria.order_pool = order_pool  # ← привязываем

# Добавляем заказы
for i in range(10):
    order_pool.add_order("margarita", 0, max_wait=60)  # правильное имя!

clock = Clock()
scheduler = Scheduler()

# Привязываем clock
pizzeria.clock = clock

sim = SimulatorEngine(pizzeria, order_pool, clock, scheduler)
sim.run(total_minutes=120)  # 2 часа, чтобы успело приготовить
