class Production:
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria

    def can_cook(self, recipe: str) -> bool:
        # пока упрощённо
        return True

    def cook(self, order):
        order.status = order.status.COOKING

        # время приготовления (пока фикс)
        cook_time = 12  # минут

        return cook_time
