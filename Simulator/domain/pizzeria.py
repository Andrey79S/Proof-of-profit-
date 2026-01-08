# domain/pizzeria.py

from core.config_loader import ConfigLoader
from domain.equipment import EquipmentFactory
from domain.staff import StaffFactory
from domain.inventory import Inventory
from domain.product import DoughBatch  # ← Добавлен импорт!
from engine.production import ProductionEngine


class Pizzeria:
    def __init__(self, config_path: str = "config"):
        loader = ConfigLoader(config_path)
        configs = loader.load_all()

        self.economy = configs.get("economy", {})
        self.recipes = configs.get("recipes", {})
        self.equipment = {
            name: EquipmentFactory.create_from_json(data)
            for name, data in configs.get("equipment", {}).items()
        }
        self.staff = {
            name: StaffFactory.create_from_json(data)
            for name, data in configs.get("staff", {}).items()
        }

        self.inventory = Inventory()
        self.production_engine = ProductionEngine(self)

        self.energy_consumed = 0.0
        self.revenue = 0.0
        self.expenses = 0.0
        self.losses = 0.0

        self.order_pool = None   # будет установлено в run.py
        self.clock = None         # будет установлено в симуляторе

    def can_accept_order(self, order):
        recipe = self.recipes.get(order.recipe)
        if not recipe:
            return False

        now = self.clock.now() if self.clock else 0

        # Проверка ингредиентов (кроме теста)
        for ing_name, qty in recipe.get("ingredients", {}).items():
            if ing_name == "dough":
                continue
            ing = self.inventory.ingredients.get(ing_name)
            if not ing or ing.amount_kg < qty:
                return False

        # Проверка теста
        dough_needed = recipe.get("dough", 0.25)
        available_dough = sum(
            b.amount_kg for b in self.inventory.dough_batches
            if not b.is_expired(now)
        )
        if available_dough < dough_needed:
            return False

        return True
def cook(self, order, now: int):
    recipe = self.recipes[order.recipe]
        # Потребление со стола
    for ing, qty in recipe["ingredients"].items():
        self.inventory.consume_ingredient(ing, qty)  # берёт со стола сначала
    self.inventory.consume_dough(recipe.get("dough", 0.25), now)
        
        # Учёт скорости персонала
        staff_speed = next(
            (s.speed_multiplier for s in self.staff.values() if s.role == "cook"),
            1.0
        )
        assembly_time = recipe.get("assembly_time_min", 3) / staff_speed

        # Время в печи (берём из оборудования)
        oven = self.equipment.get("oven_basic")
        cook_time = oven.cook_time_min if oven else 10

        total_time = int(assembly_time + cook_time)

        # Потребление ингредиентов
        for ing_name, qty in recipe.get("ingredients", {}).items():
            if ing_name != "dough":
                self.inventory.consume_ingredient(ing_name, qty)

        # Потребление теста
        dough_used = recipe.get("dough", 0.25)
        self.inventory.consume_dough(dough_used, now)

        # Энергия (все включённые устройства)
        active_power = sum(
            eq.power_kw for eq in self.equipment.values()
            if eq.type in ["oven", "mixer", "fridge"]
        )
        self.energy_consumed += active_power * (total_time / 60.0)
        electricity_price = self.economy.get("electricity_price_per_kwh", 0.12)
        self.expenses += active_power * (total_time / 60.0) * electricity_price

        # Доход
        self.revenue += recipe.get("price", 8.0)

        return total_time

    def add_initial_inventory(self):
        """Начальный запас для теста симуляции"""
        self.inventory.add_ingredient("tomato_sauce", 50.0)
        self.inventory.add_ingredient("mozzarella", 50.0)
        self.inventory.add_ingredient("pepperoni", 20.0)

        # Добавляем большую партию теста (100 кг, срок годности 1440 минут = 24 часа)
        initial_batch = DoughBatch(amount_kg=100.0, prepared_at_min=0, expires_at_min=1440)
        self.inventory.add_dough_batch(initial_batch)
