def calculate_energy(pizzeria, minutes: int):
    power = 0.5  # холодильники
    kwh = power * (minutes / 60)
    cost = kwh * pizzeria.config["economy"]["electricity_price_per_kwh"]
    pizzeria.finance.add_expense(cost)
