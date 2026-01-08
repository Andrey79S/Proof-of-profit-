from core.config_loader import ConfigLoader
from domain.equipment import EquipmentFactory
from domain.staff import StaffFactory
from domain.pizzeria_state import PizzeriaState
from engine.production_engine import ProductionEngine

class Pizzeria:
    def __init__(self, config_path="config"):
        loader = ConfigLoader(config_path)
        configs = loader.load_all()

        # Оборудование
        self.equipment = {name: EquipmentFactory.create_from_json(configs["equipment"][name]) for name in configs["equipment"]}

        # Стафф (если папка staff пуста, добавь JSON как в equipment)
        self.staff = {name: StaffFactory.create_from_json(configs["staff"][name]) for name in configs["staff"]} if "staff" in configs else {}

        # Рецепты
        self.recipes = configs["recipes"]

        # Состояние
        self.state = PizzeriaState()
        self.state.equipment.equipment = {eq.name: {"count": 1} for eq in self.equipment.values()}  # Пример: 1 единица каждого
        self.state.staff.staff = {st.name: {"level": st.skill_level, "speed": st.speed_modifier} for st in self.staff.values()}

        # Engine
        self.production_engine = ProductionEngine(self.recipes, configs["equipment"])

    def can_accept_order(self, order):
        return self.production_engine.can_cook(self.state, order, 0)  # now_min=0 для простоты

    def cook(self, order):
        # Учёт staff speed (берём первого cook)
        speed = next((s["speed"] for s in self.state.staff.staff.values() if "cook" in s), 1.0)
        cook_time = self.production_engine.cook(self.state, order, 0) / speed
        return int(cook_time)
