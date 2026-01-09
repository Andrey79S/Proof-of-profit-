def calculate_economics(orders_done: int, pizzeria, config: dict):
    revenue = orders_done * config["price_per_order"]

    ingredient_cost = (
        orders_done
        * config["ingredient_kg_per_order"]
        * config["ingredient_price_per_kg"]
    )

    energy_cost = (
        orders_done
        * config["energy_kwh_per_order"]
        * config["energy_price_per_kwh"]
    )

    base_expenses = ingredient_cost + energy_cost
    expenses = base_expenses * pizzeria.cost_multiplier()

    return revenue, expenses, {
        "ingredients_kg": orders_done * config["ingredient_kg_per_order"],
        "energy_kwh": orders_done * config["energy_kwh_per_order"],
    }
