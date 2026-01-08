# domain/pizzeria.py

from core.config_loader import ConfigLoader
from domain.equipment import EquipmentFactory
from domain.staff import StaffFactory
from domain.inventory import Inventory  # ← Добавлен импорт
from domain.product import DoughBatch  # если нужен
from engine.production import ProductionEngine  # или production_engine, если так называется

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

        self.order_pool = None
        self.clock = None

    def can_accept_order(self, order) -> bool:
        recipe = self.recipes.get(order.recipe)
        if not recipe:
            return False

        now = self.clock.now() if self.clock else 0

        # Проверка ингредиентов
        for ing_name, qty in recipe.get("ingredients", {}).items():
            if ing_name == "dough":
                continue
            total = 0.0
            if ing_name in self.inventory.ingredients:
                total += self.inventory.ingredients[ing_name].amount_kg
            if total < qty:
                return False

        # Проверка теста (готовое — после расстойки)
        dough_needed = recipe.get("dough", 0.25)
        available = sum(b.amount_kg for b in self.inventory.dough_batches if not b.is_expired(now))
        return available >= dough_needed

    def cook(self, order, now: int) -> int:
        recipe = self.recipes[order.recipe]

        staff_speed = next((s.speed_multiplier for s in self.staff.values() if s.role == "cook"), 1.0)
        assembly_time = recipe.get("assembly_time_min", 3) / staff_speed

        oven = next((eq for eq in self.equipment.values() if eq.type == "oven"), None)
        cook_time = oven.cook_time_min if oven else 10

        total_time = int(assembly_time + cook_time)

        # Тратим ингредиенты
        for ing, qty in recipe.get("ingredients", {}).items():
            if ing != "dough":
                self.inventory.consume_ingredient(ing, qty)
        self.inventory.consume_dough(recipe.get("dough", 0.25), now)

        # Энергия
        power = oven.power_kw if oven else 8.0
        self.energy_consumed += power * (total_time / 60)
        self.expenses += power * (total_time / 60) * self.economy.get("electricity_price_per_kwh", 0.12)

        self.revenue += recipe.get("price", 8.0)

        return total_time

    def add_initial_inventory(self):
        self.inventory.add_ingredient("tomato_sauce", 200.0)
        self.inventory.add_ingredient("mozzarella", 200.0)
        self.inventory.add_ingredient("pepperoni", 100.0)
        self.inventory.add_ingredient("flour", 500.0)
        self.inventory.add_ingredient("water", 300.0)
        self.inventory.add_ingredient("salt", 20.0)
        self.inventory.add_ingredient("yeast", 10.0)
        self.inventory.add_ingredient("olive_oil", 10.0)

        # Начальное готовое тесто
        batch = DoughBatch(amount_kg=100.0, prepared_at_min=0, expires_at_min=2880)
        self.inventory.dough_batches.append(batch)
