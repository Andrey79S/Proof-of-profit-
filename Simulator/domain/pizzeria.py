from domain.equipment import EquipmentFactory

class Pizzeria:
    def __init__(self, equipment_configs, recipe_configs, staff_configs):
        self.equipment = {}
        for name, path in equipment_configs.items():
            self.equipment[name] = EquipmentFactory.create_from_json(path)
        # остальная инициализация...
