from engine.pizzeria import Pizzeria

pizzeria = Pizzeria()
report = pizzeria.simulate_day(
    margarita_qty=40,
    pepperoni_qty=30
)

print(report)
