def calculate_economics_by_pizza(pizza_orders: dict, menu, pizzeria) -> dict:
    """
    Возвращает доход, расходы, ингредиенты, энергию по типам пицц
    """
    revenue = 0.0
    ingredient_cost = 0.0
    energy_cost = 0.0
    ingredients_used = 0.0
    energy_used = 0.0

    for pizza_type, qty in pizza_orders.items():
        info = menu.types[pizza_type]
        revenue += qty * info["price"]
        ing_cost = qty * info["ingredient_kg"] * info.get("ingredient_price_per_kg", 13)
        eng_cost = qty * info["energy_kwh"] * info.get("energy_price_per_kwh", 1.25)
        ingredient_cost += ing_cost
        energy_cost += eng_cost
        ingredients_used += qty * info["ingredient_kg"]
        energy_used += qty * info["energy_kwh"]

    # применяем коэффициент экономической эффективности апгрейдов
    multiplier = pizzeria.cost_multiplier()
    total_expenses = (ingredient_cost + energy_cost) * multiplier

    return {
        "revenue": revenue,
        "expenses": total_expenses,
        "ingredients_used_kg": ingredients_used,
        "energy_used_kwh": energy_used,
        "details": {
            "per_pizza_type": pizza_orders,
            "ingredient_cost": ingredient_cost,
            "energy_cost": energy_cost,
            "multiplier": multiplier
        }
    }
