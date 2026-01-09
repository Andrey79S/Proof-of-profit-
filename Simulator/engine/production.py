# engine/production.py

class ProductionEngine:
    """
    Движок производства: готовка пиццы, списание ингредиентов, учёт времени и энергии
    """
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria  # Ссылка на агрегат Pizzeria

    def cook_order(self, order):
        """
        Готовим заказ полностью.
        Возвращает время готовки в минутах.
        """
        now = self.pizzeria.clock.now() if self.pizzeria.clock else 0

        if not self.pizzeria.can_accept_order(order):
            return 0

        # Вызов метода Pizzeria для готовки
        total_time = self.pizzeria.cook(order, now)

        return total_time
