from domain.pizzeria import Pizzeria
from domain.order_pool import OrderPool
from domain.order import Order
from engine.simulator import Clock, SimulatorEngine
from domain.pizzeria_state import DoughBatch

# Инициализация
pizzeria = Pizzeria(config_path="Simulator/config")  # Путь к config

# Пример инвентаря
pizzeria.state.inventory.ingredients = {"tomato_sauce": 20, "mozzarella": 20}
pizzeria.state.inventory.dough_batches = [DoughBatch(10, 0, 100)]  # amount, prepared, expires

# Пул заказов (задай вручную)
order_pool = OrderPool()
for i in range(5):  # 5 заказов
    order_pool.add_order("margarita", 0, max_wait=30)

# Симулятор
clock = Clock()
sim = SimulatorEngine(pizzeria, order_pool, clock)
sim.run(sessions=1, hours_per_session=1)  # 1 сессия по 1 часу
