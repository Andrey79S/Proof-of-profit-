class Menu:
    def __init__(self):
        # базовые типы пицц
        self.types = {
            "basic": {"price": 10},
            "premium": {"price": 16}
        }
        # уровни апгрейдов меню
        self.menu_level = 1

    def convert_orders_to_pizzas(self, orders_count: int) -> dict:
        # распределение пицц в зависимости от уровня меню
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
