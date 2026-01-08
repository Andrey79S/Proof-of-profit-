import json
from domain.equipment import EquipmentFactory
from domain.staff import StaffFactory
from domain.product import Recipe

class Pizzeria:
    def __init__(self, equipment_files, staff_files, recipe_files):
        # Загружаем оборудование
        self.equipment = {
            name: EquipmentFactory.create_from_json(path)
            for name, path in equipment_files.items()
        }
        print("Оборудование загружено:", self.equipment.keys())

        # Загружаем стафф
        self.staff = {
            name: StaffFactory.create_from_json(path)
            for name, path in staff_files.items()
        }
        print("Стафф загружен:", self.staff.keys())

        # Загружаем рецепты
        self.recipes = {
            name: Recipe.from_json(path)
            for name, path in recipe_files.items()
        }
        print("Рецепты загружены:", self.recipes.keys())

        # Инвентарь, тесто и т.д.
        self.inventory = {}
        self.production = None  # сюда потом можно поставить ProductionEngine

    def can_accept_order(self, order):
        # Простейшая проверка: есть ли рецепт и доступное оборудование
        return order.recipe in self.recipes
