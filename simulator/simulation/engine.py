from economy.formulas import calculate_economics

def simulate_tick(pizzeria, order_pool, config, hours: float):
    capacity = pizzeria.capacity(hours)
    orders_done = order_pool.take(capacity)

    revenue, expenses = calculate_economics(orders_done, config)

    pizzeria.ledger.add_revenue(revenue)
    pizzeria.ledger.add_expense(expenses)
