# persistence/state.py

import json

class PizzeriaState:
    """
    Хранение состояния пиццерии: доход, расходы, инвентарь, тесто и т.д.
    """
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria

    def save(self, filepath):
        """
        Сохраняет текущее состояние пиццерии в JSON
        """
        data = {
            "revenue": self.pizzeria.revenue,
            "expenses": self.pizzeria.expenses,
            "losses": self.pizzeria.losses,
            "energy_consumed": self.pizzeria.energy_consumed,
            "inventory": {
                "ingredients": {k: v.amount_kg for k, v in self.pizzeria.inventory.ingredients.items()},
                "table_ingredients": {k: v.amount_kg for k, v in self.pizzeria.inventory.table_ingredients.items()},
                "dough_batches": [
                    {"amount_kg": b.amount_kg, "prepared_at_min": b.prepared_at_min, "expires_at_min": b.expires_at_min}
                    for b in self.pizzeria.inventory.dough_batches
                ],
                "table_dough": [
                    {"amount_kg": b.amount_kg, "prepared_at_min": b.prepared_at_min, "expires_at_min": b.expires_at_min}
                    for b in self.pizzeria.inventory.table_dough
                ]
            }
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self, filepath):
        """
        Загружает состояние из JSON
        """
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.pizzeria.revenue = data.get("revenue", 0.0)
        self.pizzeria.expenses = data.get("expenses", 0.0)
        self.pizzeria.losses = data.get("losses", 0.0)
        self.pizzeria.energy_consumed = data.get("energy_consumed", 0.0)

        inv = self.pizzeria.inventory

        # Ингредиенты
        for k, v in data.get("inventory", {}).get("ingredients", {}).items():
            if k in inv.ingredients:
                inv.ingredients[k].amount_kg = v
        for k, v in data.get("inventory", {}).get("table_ingredients", {}).items():
            if k in inv.table_ingredients:
                inv.table_ingredients[k].amount_kg = v

        # Тесто
        inv.dough_batches = [
            DoughBatch(**b) for b in data.get("inventory", {}).get("dough_batches", [])
        ]
        inv.table_dough = [
            DoughBatch(**b) for b in data.get("inventory", {}).get("table_dough", [])
        ]
