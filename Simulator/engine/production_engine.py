# engine/production_engine.py

from typing import Dict
from domain.pizzeria_state import PizzeriaState, DoughBatch
from domain.order import Order


class ProductionEngine:
    def __init__(self, recipes: Dict, equipment_cfg: Dict):
        self.recipes = recipes
        self.equipment_cfg = equipment_cfg

    # -----------------------------
    # МОЖЕМ ЛИ ПРИНЯТЬ ЗАКАЗ
    # -----------------------------

    def can_cook(self, state: PizzeriaState, order: Order, now_min: int) -> bool:
        recipe = self.recipes[order.recipe]

        # 1. проверка ингредиентов
        for name, qty in recipe["ingredients"].items():
            if state.inventory.ingredients.get(name, 0) < qty:
                return False

        # 2. проверка теста
        if state.inventory.total_dough() < recipe["dough"]:
            return False

        # 3. проверка оборудования
        if not self._has_required_equipment(state, recipe):
            return False

        # 4. проверка что пиццерия открыта
        if not state.is_open:
            return False

        return True

    # -----------------------------
    # ГОТОВИМ ЗАКАЗ
    # -----------------------------

    def cook(self, state: PizzeriaState, order: Order, now_min: int) -> int:
        recipe = self.recipes[order.recipe]

        # 1. списываем ингредиенты
        for name, qty in recipe["ingredients"].items():
            state.inventory.ingredients[name] -= qty

        # 2. списываем тесто
        self._consume_dough(state, recipe["dough"], now_min)

        # 3. считаем время
        cook_time = self._calculate_cook_time(recipe)

        # 4. считаем энергию
        self._consume_energy(state, cook_time)

        # 5. считаем деньги
        price = recipe["price"]
        state.finance.balance += price
        state.finance.revenue += price

        # 6. статистика
        state.stats.orders_completed += 1
        state.stats.pizzas_made[order.recipe] = (
            state.stats.pizzas_made.get(order.recipe, 0) + 1
        )

        return cook_time

    # -----------------------------
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
    # -----------------------------

    def _consume_dough(self, state: PizzeriaState, amount: int, now_min: int):
        # удаляем испорченное тесто
        state.inventory.dough_batches = [
            b for b in state.inventory.dough_batches
            if b.expires_at_min > now_min
        ]

        # берём самое старое
        state.inventory.dough_batches.sort(key=lambda b: b.prepared_at_min)

        remaining = amount
        for batch in state.inventory.dough_batches:
            if remaining <= 0:
                break
            take = min(batch.amount, remaining)
            batch.amount -= take
            remaining -= take

        # чистим пустые партии
        state.inventory.dough_batches = [
            b for b in state.inventory.dough_batches if b.amount > 0
        ]

        if remaining > 0:
            raise RuntimeError("Недостаточно теста")

    def _calculate_cook_time(self, recipe: Dict) -> int:
        oven_cfg = self.equipment_cfg["oven_basic"]
        return oven_cfg["cook_time_min"]

    def _consume_energy(self, state: PizzeriaState, cook_time_min: int):
        oven_cfg = self.equipment_cfg["oven_basic"]
        power = oven_cfg["power_kw"]

        hours = cook_time_min / 60
        state.energy.consumed_kwh += power * hours

    def _has_required_equipment(self, state: PizzeriaState, recipe: Dict) -> bool:
        for eq in recipe["equipment"]:
            if eq not in state.equipment.equipment:
                return False
        return True
