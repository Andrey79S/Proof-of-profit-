# domain/pizzeria.py

from core.config_loader import ConfigLoader
from domain.inventory import Inventory
from domain.product import DoughBatch
from domain.equipment import EquipmentFactory
from domain.staff import StaffFactory


class Pizzeria:
    def __init__(self, config_path: str = "config"):
        """
        Полный агрегат пиццерии:
        - финансы
        - инвентарь
        - персонал
        - оборудование
        - рецепты
        """
        loader = ConfigLoader(config_path)
        configs = loader.load_all()

        # Основные конфиги
        self.economy = configs.get("economy", {})
        self.recipes = configs.get("recipes", {})

        # Оборудование и персонал
        self.equipment = {
            name: EquipmentFactory.create_from_json(data)
            for name, data in configs.get("equipment", {}).items()
        }
        self.staff = {
            name: StaffFactory.create_from_json(data)
            for name, data in configs.get("staff", {}).items()
        }

        # Инвентарь
        self.inventory = Inventory()

        # Финансы
        self.revenue = 0.0
        self.expenses = 0.0
        self.losses = 0.0
        self.energy_consumed = 0.0

        # Симулятор
        self.clock = None      # Clock передаётся из run.py или app
        self.order_pool = None # Пул заказов

    # ----------------------------------------
    # Проверка доступности заказа
    # ----------------------------------------
    def can_accept_order(self, order) -> bool:
        recipe = self.recipes.get(order.recipe)
        if not recipe:
            return False

        now = self.clock.now() if self.clock else 0

        # Проверяем ингредиенты (кроме теста)
        for ing_name, qty in recipe.get("ingredients", {}).items():
            if ing_name == "dough":
                continue
            total_amount = 0.0
            if ing_name in self.inventory.ingredients:
                total_amount += self.inventory.ingredients[ing_name].amount_kg
            if ing_name in self.inventory.table_ingredients:
                total_amount += self.inventory.table_ingredients[ing_name].amount_kg
            if total_amount < qty:
                return False

        # Проверяем тесто (готовое, не просроченное)
        dough_needed = recipe.get("dough", 0.25)
        available_dough = sum(
            b.amount_kg for b in (self.inventory.dough_batches + self.inventory.table_dough)
            if not b.is_expired(now)
        )
        if available_dough < dough_needed:
            return False

        # Можно добавить проверку свободной печи и персонала
        return True

    # ----------------------------------------
    # Готовка пиццы
    # ----------------------------------------
    def cook(self, order, now: int) -> int:
        recipe = self.recipes.get(order.recipe)
        if not recipe:
            return 0

        # Скорость повара
        cook_speed = next(
            (s.speed_multiplier for s in self.staff.values() if s.role == "cook"),
            1.0
        )
        assembly_time = recipe.get("assembly_time_min", 3) / cook_speed

        # Время выпечки
        oven = next((eq for eq in self.equipment.values() if eq.type == "oven"), None)
        cook_time = oven.cook_time_min if oven else 10

        total_time = int(assembly_time + cook_time)

        # Списание ингредиентов
        for ing_name, qty in recipe.get("ingredients", {}).items():
            if ing_name != "dough":
                self.inventory.consume_ingredient(ing_name, qty)

        # Списание теста
        dough_used = recipe.get("dough", 0.25)
        self.inventory.consume_dough(dough_used, now)

        # Энергопотребление
        active_power = sum(
            eq.power_kw for eq in self.equipment.values()
            if eq.type in ["oven", "fridge", "proofing_fridge", "table_fridge"]
        )
        oven_power = oven.power_kw if oven else 0.0
        # Печь работает только во время выпечки, холодильники круглосуточно
        self.energy_consumed += (active_power - oven_power + oven_power) * (total_time / 60.0)

        # Расходы на электричество
        electricity_price = self.economy.get("electricity_price_per_kwh", 0.12)
        self.expenses += oven_power * (total_time / 60.0) * electricity_price

        # Доход
        self.revenue += recipe.get("price", 8.0)

        return total_time

    # ----------------------------------------
    # Начальный инвентарь
    # ----------------------------------------
    def add_initial_inventory(self):
        # Ингредиенты для пиццы
        self.inventory.add_ingredient("tomato_sauce", 100.0)
        self.inventory.add_ingredient("mozzarella", 100.0)
        self.inventory.add_ingredient("pepperoni", 50.0)

        # Ингредиенты для теста
        self.inventory.add_ingredient("flour", 500.0)
        self.inventory.add_ingredient("water", 300.0)
        self.inventory.add_ingredient("salt", 20.0)
        self.inventory.add_ingredient("yeast", 10.0)
        self.inventory.add_ingredient("olive_oil", 10.0)

        # Начальная партия теста
        initial_batch = DoughBatch(
            amount_kg=100.0,
            prepared_at_min=-720,  # 12 часов назад
            expires_at_min=2880 - 720 + 1440
        )
        self.inventory.table_dough.append(initial_batch)

    # ----------------------------------------
    # Круглосуточная энергия холодильников
    # ----------------------------------------
    def daily_energy_cost(self):
        fridge_power = sum(
            eq.power_kw for eq in self.equipment.values()
            if eq.type in ["fridge", "proofing_fridge", "table_fridge"]
        )
        daily_kwh = fridge_power * 24
        daily_cost = daily_kwh * self.economy.get("electricity_price_per_kwh", 0.12)
        self.energy_consumed += daily_kwh
        self.expenses += daily_cost
        return daily_cost
