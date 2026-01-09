def calculate_daily_energy(pizzeria):
    power = sum(eq.power_kw for eq in pizzeria.equipment)
    daily_kwh = power * 24
    cost = daily_kwh * pizzeria.config["economy"]["electricity_price_per_kwh"]
    pizzeria.finance["expenses"] += cost
    print(f"Ежедневные расходы на энергию: {cost:.2f}")
