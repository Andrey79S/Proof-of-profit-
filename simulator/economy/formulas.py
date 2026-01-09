def calculate_economics(orders_done: int, config: dict):
    revenue = orders_done * config["price_per_order"]

    expenses = orders_done * (
        config["ingredient_cost_per_order"]
        + config["energy_cost_per_order"]
    )

    return revenue, expenses
