from engine.production import Production

class Pizzeria:
    def __init__(self, inventory, equipment_list, staff_list):
        self.inventory = inventory
        self.equipment = equipment_list
        self.staff = staff_list

        self.production = Production(self)

    def can_accept_order(self, order):
        return True
