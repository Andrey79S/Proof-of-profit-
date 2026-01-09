# engine/energy.py

def calculate_energy(pizzeria, minutes: int):
    # Пример: холодильники 0.5 кВт круглосуточно
    power = 0.5  # кВт
    kwh = power * (minutes / 60)
    cost = kwh * pizzeria.config["economy"]["electricity_price_per_kwh"]
    pizzeria.finance.add_expense(cost)
    pizzeria.clock.tick(minutes)
