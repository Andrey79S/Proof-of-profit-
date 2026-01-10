class Menu:
    def __init__(self):
        self.types = {
            "basic": {"price": 10, "ingredient_kg": 0.3, "energy_kwh": 0.8},
            "premium": {"price": 16, "ingredient_kg": 0.5, "energy_kwh": 1.2}
        }
        self.menu_level = 1

    def convert_orders_to_pizzas(self, orders_count: int) -> dict:
        """
        Конвертация заказов в пиццы в зависимости от уровня меню
        """
        if self.menu_level == 1:
            return {"basic": orders_count}
        elif self.menu_level == 2:
            premium = int(orders_count * 0.3)
            basic = orders_count - premium
            return {"basic": basic, "premium": premium}
        else:
            premium = int(orders_count * 0.5)
            basic = orders_count - premium
            return {"basic": basic, "premium": premium}
