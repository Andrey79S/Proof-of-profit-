# persistence/state.py

import json
from typing import Dict, Any


STATE_FILE = "pizzeria_state.json"


class PizzeriaState:
    """
    DTO состояния пиццерии.
    НЕ содержит логики.
    """

    @staticmethod
    def save(pizzeria, clock) -> None:
        data: Dict[str, Any] = {
            "last_seen_minute": clock.now(),
            "finance": {
                "revenue": pizzeria.revenue,
                "expenses": pizzeria.expenses,
                "losses": pizzeria.losses,
                "energy_consumed": pizzeria.energy_consumed,
            },
            "inventory": {
                "ingredients": {
                    name: ing.amount_kg
                    for name, ing in pizzeria.inventory.ingredients.items()
                },
                "table_ingredients": {
                    name: ing.amount_kg
                    for name, ing in pizzeria.inventory.table_ingredients.items()
                },
                "dough_batches": [
                    {
                        "amount_kg": b.amount_kg,
                        "prepared_at": b.prepared_at_min,
                        "expires_at": b.expires_at_min,
                    }
                    for b in pizzeria.inventory.dough_batches
                ],
                "table_dough": [
                    {
                        "amount_kg": b.amount_kg,
                        "prepared_at": b.prepared_at_min,
                        "expires_at": b.expires_at_min,
                    }
                    for b in pizzeria.inventory.table_dough
                ],
            },
        }

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load(pizzeria, clock) -> int:
        """
        Загружает состояние в агрегат.
        Возвращает offline_delta (в минутах).
        """
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return 0

        last_seen = data.get("last_seen_minute", 0)
        offline_delta = clock.now() - last_seen

        finance = data.get("finance", {})
        pizzeria.revenue = finance.get("revenue", 0.0)
        pizzeria.expenses = finance.get("expenses", 0.0)
        pizzeria.losses = finance.get("losses", 0.0)
        pizzeria.energy_consumed = finance.get("energy_consumed", 0.0)

        inv = data.get("inventory", {})

        # Ингредиенты
        for name, amount in inv.get("ingredients", {}).items():
            pizzeria.inventory.add_ingredient(name, amount)

        for name, amount in inv.get("table_ingredients", {}).items():
            pizzeria.inventory.add_ingredient(name, amount, to_table=True)

        # Тесто
        from domain.product import DoughBatch

        for b in inv.get("dough_batches", []):
            pizzeria.inventory.dough_batches.append(
                DoughBatch(
                    amount_kg=b["amount_kg"],
                    prepared_at_min=b["prepared_at"],
                    expires_at_min=b["expires_at"],
                )
            )

        for b in inv.get("table_dough", []):
            pizzeria.inventory.table_dough.append(
                DoughBatch(
                    amount_kg=b["amount_kg"],
                    prepared_at_min=b["prepared_at"],
                    expires_at_min=b["expires_at"],
                )
            )

        return max(0, offline_delta)
