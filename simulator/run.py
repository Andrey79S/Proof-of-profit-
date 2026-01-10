from config.default import CONFIG
from domain.order_pool import OrderPool
from domain.order_reserve import OrderReserve
from domain.pizzeria import Pizzeria
from accounting.ledger import Ledger
from accounting.report import generate_report
from simulation.engine import simulate_production

# ======== Создаём рынок ========
order_pool = OrderPool(initial_orders=1000)

# ======== Создаём игрока ========
reserve = OrderReserve(base_capacity=CONFIG["max_reserve"])
ledger = Ledger()
pizzeria = Pizzeria(
    base_capacity_per_hour=CONFIG["base_capacity_per_hour"],
    reserve=reserve,
    ledger=ledger
)
pizzeria.day = 12  # для отчёта

# ======== Игрок тапает (добавляет заказы в пул) ========
taps = 20
taken_from_pool = order_pool.take(taps * pizzeria.tap_power())
reserve.add(taken_from_pool, pizzeria)

# ======== Конвертация заказов в пиццы и производство ========
simulate_production(pizzeria, hours=24)  # имитируем 1 день

# ======== Генерация отчёта ========
report = generate_report(pizzeria)
print(report)

# ======== Остаток заказов в пуле ========
print("\nOrders left in pool:", order_pool.orders)
