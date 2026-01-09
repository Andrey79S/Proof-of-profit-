from economy.formulas import calculate_economics

def simulate_time(pizzeria, config, hours: float):
    max_possible = pizzeria.production_capacity(hours)
    executed = pizzeria.reserve.consume(max_possible)

    if executed <= 0:
        return

    revenue, expenses, flows = calculate_economics(executed, config)

    pizzeria.ledger.add_revenue(revenue)
    pizzeria.ledger.add_expense(expenses)

    pizzeria.ledger.ingredients_used += flows["ingredients_kg"]
    pizzeria.ledger.energy_used += flows["energy_kwh"]
