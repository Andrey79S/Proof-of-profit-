class Pizzeria:
    def __init__(self, inventory, equipment, staff):
        self.inventory = inventory
        self.equipment = equipment
        self.staff = staff

        self.money = 0.0
        self.energy_used = 0.0

        from engine.production import Production
        self.production = Production(self)

    def can_accept_order(self, order):
        return self.production.can_cook(order.recipe)
