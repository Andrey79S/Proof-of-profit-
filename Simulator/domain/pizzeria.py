# В методе can_accept_order(self, order):

def can_accept_order(self, order):
    recipe = self.recipes.get(order.recipe)
    if not recipe:
        return False

    now = 0  # или self.clock.now(), если clock привязан

    # Проверка ингредиентов (кроме теста)
    for ing_name, qty in recipe["ingredients"].items():
        if ing_name == "dough":
            continue
        ing = self.inventory.ingredients.get(ing_name)
        if not ing or ing.amount_kg < qty:
            return False

    # Проверка теста
    dough_needed = recipe.get("dough", 0.25)
    available_dough = sum(
        b.amount_kg for b in self.inventory.dough_batches
        if not b.is_expired(now)
    )
    if available_dough < dough_needed:
        return False

    # Можно добавить: проверка свободного оборудования и персонала
    return True
