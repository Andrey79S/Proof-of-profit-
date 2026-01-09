# domain/pizzeria.py

from core.config_loader import ConfigLoader
from domain.inventory import Inventory
from domain.product import DoughBatch
from engine.production import ProductionEngine
from domain.equipment import EquipmentFactory
from domain.staff import StaffFactory


class Finance:
    def __init__(self):
        self.revenue: float = 0.0
        self.expenses: float = 0.0
        self.losses: float = 0.0

    def net_profit(self) -> float:
        return self.revenue - self.expenses - self.losses


class Pizzeria:
    def __init__(self, config_path: str = "config"):
        self.loader = ConfigLoader(config_path)
        self.config = {
            "economy": self.loader.load("economy.json"),
            "recipes": self.loader.load_dir("recipes"),
            "equipment": self.loader.load_dir("equipment"),
            "staff": self.loader.load_dir("staff"),
        }

        # Фабрики
        self.equipment = {
            name: EquipmentFactory.create_from_json(data)
            for name, data in self.config["equipment"].items()
        }

        self.staff = {
            name: StaffFactory.create_from_json(data)
            for name, data in self.config["staff"].items()
        }

        # Основные компоненты
        self.inventory = Inventory()
        self.finance = Finance()
        self.production_engine = ProductionEngine(self)

        # Ссылки на внешние объекты (устанавливаются позже)
        self.clock = None
        self.order_pool = None

        # Начальный инвентарь (можно вынести в отдельный метод)
        self._initialize_inventory()

    def _initialize_inventory(self):
        """Начальный запас для тестов и запуска"""
        # Ингредиенты для пицц
        self.inventory.add_ingredient("tomato_sauce", 100.0)
        self.inventory.add_ingredient("mozzarella", 100.0)
        self.inventory.add_ingredient("pepperoni", 50.0)

        # Ингредиенты для теста
        self.inventory.add_ingredient("flour", 500.0)
        self.inventory.add_ingredient("water", 300.0)
        self.inventory.add_ingredient("salt", 20.0)
        self.inventory.add_ingredient("yeast", 10.0)
        self.inventory.add_ingredient("olive_oil", 10.0)

        # Начальная партия готового теста (чтобы сразу можно было готовить)
        initial_batch = DoughBatch(
            amount_kg=50.0,
            prepared_at_min=-720,  # уже расстоялось
            expires_at_min=2880 - 720 + 1440  # срок хранения после расстойки
        )
        self.inventory.add_dough_batch(initial_batch)

    def can_accept_order(self, recipe_name: str) -> bool:
        """Можно ли сейчас принять заказ на эту пиццу"""
        recipe = self.config["recipes"].get(recipe_name)
        if not recipe:
            return False

        now = self.clock.now() if self.clock else 0

        # Проверка ингредиентов (кроме теста)
        for ing_name, qty in recipe.get("ingredients", {}).items():
            if ing_name == "dough":
                continue
            available = self.inventory.ingredients.get(ing_name, 0.0)
            if available < qty:
                return False

        # Проверка теста (готового, не истёкшего)
        dough_needed = recipe.get("dough_kg", 0.25)
        available_dough = sum(
            b.amount_kg for b in self.inventory.dough_batches
            if not b.is_expired(now)
        )
        if available_dough < dough_needed:
            return False

        # Можно добавить проверку свободной печи/персонала
        return True

    def cook(self, recipe_name: str):
        """Приготовление одной пиццы"""
        recipe = self.config["recipes"][recipe_name]
        now = self.clock.now()

        # Списание ингредиентов (со стола/холодильника)
        for ing_name, qty in recipe.get("ingredients", {}).items():
            if ing_name != "dough":
                self.inventory.consume_ingredient(ing_name, qty)

        # Списание теста
        dough_used = recipe.get("dough_kg", 0.25)
        self.inventory.consume_dough(dough_used, now)

        # Время приготовления (пример)
        assembly_time = recipe.get("assembly_time_min", 3)
        cook_time = next(
            (eq.cook_time_min for eq in self.equipment.values() if eq.type == "oven"),
            10
        )
        total_time = assembly_time + cook_time
        self.clock.tick(total_time)

        # Доход
        price = recipe.get("price", 12.0)
        self.finance.revenue += price

        # Энергия (упрощённо)
        oven_power = next((eq.power_kw for eq in self.equipment.values() if eq.type == "oven"), 8.0)
        self.finance.expenses += oven_power * (total_time / 60) * self.config["economy"]["electricity_price_per_kwh"]

        print(f"Приготовлена {recipe_name} за {price:.2f}$ (время: {total_time} мин)")

    def __str__(self):
        return f"Pizzeria: {self.finance.revenue:.2f}$ выручка, {self.inventory.dough_batches} партий теста"
