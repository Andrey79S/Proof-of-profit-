from core.config_loader import ConfigLoader
from domain.equipment import EquipmentFactory
from domain.staff import StaffFactory
from domain.pizzeria_state import PizzeriaState
from engine.production_engine import ProductionEngine

class Pizzeria:
    def add_initial_inventory(self):
        self.inventory.add_ingredient("tomato_sauce", 100.0)
        self.inventory.add_ingredient("mozzarella", 100.0)
        self.inventory.add_ingredient("pepperoni", 50.0)
        self.inventory.add_ingredient("flour", 500.0)
        self.inventory.add_ingredient("water", 300.0)
        self.inventory.add_ingredient("salt", 20.0)
        self.inventory.add_ingredient("yeast", 10.0)
        self.inventory.add_ingredient("olive_oil", 10.0)

        # Начальное готовое тесто
        batch = DoughBatch(100.0, -720, 2880)
        self.inventory.table_dough.append(batch)
    def __init__(self, config_path: str = "config"):
        loader = ConfigLoader(config_path)
        configs = loader.load_all()

        self.economy = configs.get("economy", {})
        self.recipes = configs.get("recipes", {})
        self.equipment = {name: EquipmentFactory.create_from_json(data) for name, data in configs.get("equipment", {}).items()}
        self.staff = {name: StaffFactory.create_from_json(data) for name, data in configs.get("staff", {}).items()}

        self.inventory = Inventory()
        self.production_engine = ProductionEngine(self)

        self.energy_consumed = 0.0
        self.revenue = 0.0
        self.expenses = 0.0
        self.losses = 0.0

        self.order_pool = None
        self.clock = None
    def can_accept_order(self, order):
        return self.production_engine.can_cook(self.state, order, 0)  # now_min=0 для простоты

    def cook(self, order):
        # Учёт staff speed (берём первого cook)
        speed = next((s["speed"] for s in self.state.staff.staff.values() if "cook" in s), 1.0)
        cook_time = self.production_engine.cook(self.state, order, 0) / speed
        return int(cook_time)
