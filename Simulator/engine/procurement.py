import json
import os
import random
from domain.equipment import EquipmentFactory

class Procurement:
    def __init__(self, equipment_folder="config/equipment", delivery_time=1):
        """
        delivery_time — время доставки в минутах (можно сделать игровым, сокращённым)
        """
        self.equipment_folder = equipment_folder
        self.delivery_time = delivery_time  # в минутах

    def restock_ingredient(self, ingredient, quantity, table_fridge):
        """
        Пополняем холодильник ингредиентов.
        table_fridge — объект холодильника рабочего стола
        """
        print(f"Заказано {quantity} кг {ingredient}, доставка через {self.delivery_time} мин")
        # эмуляция времени доставки
        table_fridge.add_stock(ingredient, quantity)

    def auto_restock(self, table_fridge):
        """
        Автоматическая проверка и пополнение всех ингредиентов на столе
        """
        for ing, qty in table_fridge.current_load.items():
            if qty <= 0:
                # Определяем сколько заказывать (рандом от 1 до 5 кг)
                order_qty = random.uniform(1, 5)
                self.restock_ingredient(ing, order_qty, table_fridge)

    def restock_from_config(self, table_fridge, config_file="config/economy.json"):
        """
        Можно загружать стоимость и стандартные нормы закупки из config
        """
        if not os.path.exists(config_file):
            print("Конфиг экономики не найден!")
            return

        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Стандартная закупка всех ингредиентов
        for ing, params in data.get("ingredients", {}).items():
            if table_fridge.current_load.get(ing, 0) <= 0:
                qty = params.get("default_order", 2)  # кг
                self.restock_ingredient(ing, qty, table_fridge)
