from config.default import CONFIG
from domain.order_pool import OrderPool
from domain.order_reserve import OrderReserve
from domain.pizzeria import Pizzeria
from accounting.ledger import Ledger
from accounting.report import generate_report
from simulation.engine import simulate_time

# рынок
order_pool = OrderPool(initial_orders=1000)

# игрок
reserve = OrderReserve(max_capacity=CONFIG["max_reserve"])
ledger = Ledger()
pizzeria = Pizzeria(
    capacity_per_hour=CONFIG["base_capacity_per_hour"],
    reserve=reserve,
    ledger=ledger
)

# игрок тапает 20 раз
taps = 20
taken_from_pool = order_pool.take(taps * CONFIG["tap_power"])
reserve.add(taken_from_pool)

# игрок оффлайн 3 дня
simulate_time(pizzeria, CONFIG, hours=24 * 3)

print(generate_report(pizzeria))
print("Orders left in pool:", order_pool.orders)
