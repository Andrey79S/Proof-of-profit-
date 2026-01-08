from domain.equipment import EquipmentFactory
from domain.staff import Staff

class Pizzeria:
    def __init__(self, equipment_configs, staff_configs, recipes):
        self.equipment = {name: EquipmentFactory.create_from_json(path)
                          for name, path in equipment_configs.items()}

        self.staff = {name: Staff(name, skills=cfg.get("skills", {}))
                      for name, cfg in staff_configs.items()}

        self.recipes = recipes
        self.inventory = {ing: 100 for recipe in recipes.values() for ing in recipe["ingredients"]}  # стартовые запасы
        self.electricity_consumed = 0
        self.completed_orders = 0

    def can_accept_order(self, order):
        recipe = self.recipes[order.recipe]
        # проверка ингредиентов
        for ing, qty in recipe["ingredients"].items():
            if self.inventory.get(ing, 0) < qty:
                return False
        return True

    def cook(self, order):
        recipe = self.recipes[order.recipe]
        oven = self.equipment["oven_basic"]
        cook_time = oven.cook_time_min
        # расход ингредиентов
        for ing, qty in recipe["ingredients"].items():
            self.inventory[ing] -= qty
        # потребление электроэнергии
        self.electricity_consumed += oven.power_kw * cook_time / 60
        self.completed_orders += 1
        return cook_time
