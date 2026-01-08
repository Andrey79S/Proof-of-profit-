# domain/pizzeria_state.py

from dataclasses import dataclass, field
from typing import Dict, List


# -----------------------------
# ТЕСТО
# -----------------------------

@dataclass
class DoughBatch:
    """Партия теста"""
    amount: int                  # сколько порций теста
    prepared_at_min: int         # минута, когда замешано
    expires_at_min: int          # минута, когда испортится


# -----------------------------
# ИНВЕНТАРЬ
# -----------------------------

@dataclass
class InventoryState:
    ingredients: Dict[str, int] = field(default_factory=dict)
    dough_batches: List[DoughBatch] = field(default_factory=list)

    def total_dough(self) -> int:
        return sum(batch.amount for batch in self.dough_batches)


# -----------------------------
# ЭНЕРГИЯ
# -----------------------------

@dataclass
class EnergyState:
    consumed_kwh: float = 0.0


# -----------------------------
# ФИНАНСЫ
# -----------------------------

@dataclass
class FinanceState:
    balance: float = 0.0
    revenue: float = 0.0
    expenses: float = 0.0


# -----------------------------
# СТАТИСТИКА
# -----------------------------

@dataclass
class StatisticsState:
    pizzas_made: Dict[str, int] = field(default_factory=dict)
    orders_completed: int = 0
    orders_failed: int = 0


# -----------------------------
# ОБОРУДОВАНИЕ
# -----------------------------

@dataclass
class EquipmentState:
    """Хранит установленные единицы оборудования"""
    equipment: Dict[str, dict] = field(default_factory=dict)
    # пример:
    # {
    #   "oven_basic": {"count": 1},
    #   "fridge_basic": {"count": 1}
    # }


# -----------------------------
# ПЕРСОНАЛ
# -----------------------------

@dataclass
class StaffState:
    staff: Dict[str, dict] = field(default_factory=dict)
    # пример:
    # {
    #   "cook": {"level": 1, "speed": 1.0}
    # }


# -----------------------------
# СОСТОЯНИЕ ПИЦЦЕРИИ
# -----------------------------

@dataclass
class PizzeriaState:
    inventory: InventoryState = field(default_factory=InventoryState)
    energy: EnergyState = field(default_factory=EnergyState)
    finance: FinanceState = field(default_factory=FinanceState)
    stats: StatisticsState = field(default_factory=StatisticsState)
    equipment: EquipmentState = field(default_factory=EquipmentState)
    staff: StaffState = field(default_factory=StaffState)

    is_open: bool = False
    last_update_min: int = 0
