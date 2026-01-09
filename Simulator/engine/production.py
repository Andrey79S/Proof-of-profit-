def cook_pizza(pizzeria, recipe_name: str):
    if pizzeria.can_accept_order(recipe_name):
        pizzeria.cook(recipe_name)
        print(f"Приготовлена пицца: {recipe_name}")
    else:
        print(f"Нельзя приготовить {recipe_name} — недостаточно ресурсов")
