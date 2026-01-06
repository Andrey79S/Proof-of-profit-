class Pizzeria:
    def __init__(self, inventory, equipment_list, staff_list):
        self.inventory = inventory
        self.equipment = equipment_list
        self.staff = staff_list

    def can_accept_order(self, order):
        # Заглушка: проверка ресурсов
        return True
