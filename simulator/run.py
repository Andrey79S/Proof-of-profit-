from config.default import CONFIG
from domain.order_pool import OrderPool
from domain.pizzeria import Pizzeria
from accounting.ledger import Ledger
from accounting.report import generate_report
from simulation.engine import simulate_tick

ledger = Ledger()
pizzeria = Pizzeria(
    capacity_per_hour=CONFIG["base_capacity_per_hour"],
    ledger=ledger
)

order_pool = OrderPool(initial_orders=1000)

# симулируем 1 день
simulate_tick(pizzeria, order_pool, CONFIG, hours=24)

report = generate_report(ledger)
print(report)
