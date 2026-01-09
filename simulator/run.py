from config.default import CONFIG
from domain.order_pool import OrderPool
from domain.order_reserve import OrderReserve
from domain.pizzeria import Pizzeria
from accounting.ledger import Ledger
from accounting.report import generate_report
from simulation.engine import simulate_time

# создаём рынок
order_pool = OrderPool(initial_orders=1000)

# создаём игрока
reserve = OrderReserve(base_capacity=CONFIG["max_reserve"])
ledger = Ledger()
pizzeria = Pizzeria(
    base_capacity_per_hour=CONFIG["base_capacity_per_hour"],
    reserve=reserve,
    ledger=ledger
)

# игрок тапает
taps = 20
taken_from_pool = order_pool.take(taps * pizzeria.tap_power())
reserve.add(taken_from_pool, pizzeria)

# конвертируем заказы в пиццы
pizza_orders = pizzeria.menu.convert_orders_to_pizzas(reserve.current)
print("Pizza orders to produce:", pizza_orders)

# игрок оффлайн 3 дня
simulate_time(pizzeria, CONFIG, hours=24*3)

# отчёт
report = generate_report(pizzeria)
print(report)
print("Orders left in pool:", order_pool.orders)
