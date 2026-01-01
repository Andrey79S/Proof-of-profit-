from engine.pizzeria import Pizzeria

pizzeria = Pizzeria()

log = pizzeria.simulate_day(
    margarita_qty=40,
    pepperoni_qty=30,
    ingredient_purchases={
        "tomato_sauce": 10,
        "mozzarella": 10,
        "pepperoni": 5
    }
)

print(log)
