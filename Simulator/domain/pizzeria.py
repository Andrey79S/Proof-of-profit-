# domain/pizzeria.py
class Pizzeria:
    def __init__(self, equipment_list, staff_list, inventory):
        self.equipment = equipment_list
        self.staff = staff_list
        self.inventory = inventory
        self.production = None  # подключается engine.production

    def can_accept_order(self, order):
        # проверяем ингредиенты
        try:
            for ing, amt in order.recipe["ingredients"].items():
                self.inventory.consume(ing, 0)  # проверка
        except:
            return False
        # проверка staff/equipment
        return True
