from economy.formulas import calculate_economics_by_pizza

def simulate_production(pizzeria, hours: float):
    # сколько можем произвести
    capacity = pizzeria.production_capacity(hours)
    produced_orders = pizzeria.reserve.consume(capacity)
    if produced_orders <= 0:
        return

    # конвертируем в пиццы
    pizza_orders = pizzeria.menu.convert_orders_to_pizzas(produced_orders)

    # экономические расчёты
    econ_data = calculate_economics_by_pizza(pizza_orders, pizzeria.menu, pizzeria)

    # сохраняем в ledger
    pizzeria.ledger.add(econ_data)
