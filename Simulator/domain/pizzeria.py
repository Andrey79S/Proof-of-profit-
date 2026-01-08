from core.config_loader import ConfigLoader
from domain.equipment import EquipmentFactory
from domain.staff import StaffFactory
from domain.inventory import Inventory
from domain.product import Pizza
from engine.production import ProductionEngine

class Pizzeria:
    def __init__(self, config_path: str = "config"):
        loader = ConfigLoader(config_path)
        configs = loader.load_all()

        self.economy = configs["economy"]
        self.recipes = configs["recipes"]
        self.equipment = {name: EquipmentFactory.create_from_json(data) for name, data in configs["equipment"].items()}
        self.staff = {name: StaffFactory.create_from_json(data) for name, data in configs["staff"].items()}

        self.inventory = Inventory()
        self.production_engine = ProductionEngine(self)
        self.energy_consumed = 0.0
        self.revenue = 0.0
        self.expenses = 0.0
        self.losses = 0.0

    def can_accept_order(self, order):
        recipe = self.recipes.get(order.recipe)
        if not recipe:
            return False
        # Проверка ингредиентов, теста, оборудования, стаффа
        try:
            for ing, qty in recipe["ingredients"].items():
                self.inventory.consume_ingredient(ing, qty)  # Проверка, rollback если нет
            self.inventory.consume_dough(recipe.get("dough", 0.25), 0)  # Пример
            # Rollback
            return True
        except ValueError:
            return False

    def cook(self, order, now: int):
        recipe = self.recipes[order.recipe]
        staff_speed = next((s.speed_multiplier for s in self.staff.values() if s.role == "cook"), 1.0)
        assembly_time = recipe["assembly_time_min"] / staff_speed
        cook_time = self.equipment["oven_basic"].cook_time_min  # Пример
        total_time = int(assembly_time + cook_time)

        # Потребление
        for ing, qty in recipe["ingredients"].items():
            self.inventory.consume_ingredient(ing, qty)
        self.inventory.consume_dough(recipe.get("dough", 0.25), now)

        # Энергия
        power = sum(eq.power_kw for eq in self.equipment.values() if eq.type in ["oven", "mixer"])
        self.energy_consumed += power * (total_time / 60)  # кВт·ч
        self.expenses += self.energy_consumed * self.economy["electricity_price_per_kwh"]

        # Доход
        self.revenue += recipe["price"]

        return total_time

    def add_initial_inventory(self):
        # Для теста
        self.inventory.add_ingredient("tomato_sauce", 50.0)
        self.inventory.add_ingredient("mozzarella", 50.0)
        self.inventory.add_ingredient("pepperoni", 20.0)
        self.inventory.add_dough_batch(DoughBatch(100.0, 0, 1440))  # 1 день
