# domain/pizzeria.py

from core.config_loader import ConfigLoader
from domain.equipment import EquipmentFactory
from domain.staff import StaffFactory
from domain.inventory import Inventory
# Убираем или оставляем импорт ProductionEngine — не важно
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

        # Создаём engine, передавая self
        self.production_engine = ProductionEngine(self)

        self.energy_consumed = 0.0
        self.revenue = 0.0
        self.expenses = 0.0
        self.losses = 0.0
        self.clock = None  # будет установлен в симуляторе
