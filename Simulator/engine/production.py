import json
import os
from domain.equipment import EquipmentFactory
from domain.product import Dough, Pizza

class Production:
    def __init__(self, equipment_folder="config/equipment"):
        # Загружаем оборудование
        self.equipment = {}
        for fname in os.listdir(equipment_folder):
            if fname.endswith(".json"):
                with open(os.path.join(equipment_folder, fname), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    eq = EquipmentFactory.create(data)
                    self.equipment[eq.name] = eq

        # Текущее состояние теста и пицц
        self.dough_stock = 0.0  # кг
        self.pizza_stock = {}   # {"margarita": 0, "pepperoni": 0}

    def mix_dough(self, amount_kg):
        """Производим тесто, учитывая миксер и холодильник для теста"""
        mixer = self.get_equipment_by_type("mixer")
        proof_fridge = self.get_equipment_by_type("proof_fridge")

        if not mixer or not proof_fridge:
            print("Нет оборудования для замеса теста!")
            return 0.0

        # Проверяем вместимость
        batch = min(amount_kg, mixer.capacity, proof_fridge.capacity)
        self.dough_stock += batch

        # Энергопотребление
        mixer.consume_energy()
        proof_fridge.consume_energy()

        print(f"Замес: {batch} кг теста")
        return batch

    def cook(self, order):
        """Готовим пиццу, учитывая наличие теста, ингредиентов, печь"""
        pizza_type = order.recipe
        oven = self.get_equipment_by_type("oven")
        table_fridge = self.get_equipment_by_type("table_fridge")

        # Проверяем тесто
        dough_needed = Pizza.recipes[pizza_type]["dough"]
        if self.dough_stock < dough_needed:
            print(f"Недостаточно теста для {pizza_type}")
            return 1  # Минимальное время ожидания

        # Проверяем ингредиенты
        ingredients_needed = Pizza.recipes[pizza_type].copy()
        ingredients_needed.pop("dough")
        for ing, qty in ingredients_needed.items():
            if table_fridge.current_load.get(ing, 0) < qty:
                print(f"Нет ингредиента {ing} для {pizza_type}")
                return 1

        # Списываем тесто и ингредиенты
        self.dough_stock -= dough_needed
        for ing, qty in ingredients_needed.items():
            table_fridge.current_load[ing] -= qty

        # Энергопотребление
        oven.consume_energy()
        table_fridge.consume_energy()

        # Время выпечки (в минутах)
        cook_time = 8  # Можно сделать динамическим в зависимости от oven
        print(f"Готовим {pizza_type} ({cook_time} мин)")
        return cook_time

    def get_equipment_by_type(self, eq_type):
        for eq in self.equipment.values():
            if eq.type == eq_type:
                return eq
        return None
