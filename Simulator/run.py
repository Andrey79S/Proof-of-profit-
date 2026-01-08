from domain.pizzeria import Pizzeria
from domain.order_pool import OrderPool
from core.clock import Clock
from core.scheduler import Scheduler
from engine.simulator import SimulatorEngine

# Инициализация
pizzeria = Pizzeria(config_path="config")
pizzeria.add_initial_inventory()  # Начальный инвентарь

# Пул заказов
order_pool = OrderPool()
for i in range(10):
    order_pool.add_order("margarita", 0, max_wait=60)  # Правильное имя

# Симулятор
clock = Clock()
scheduler = Scheduler()
sim = SimulatorEngine(pizzeria, order_pool, clock, scheduler)
sim.run(total_minutes=60)  # 1 час
