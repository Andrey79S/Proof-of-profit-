# run.py

from core.clock import Clock
from persistence.state import PizzeriaState
from domain.pizzeria import Pizzeria
from domain.inventory import Inventory
from domain.product import DoughBatch
from app.offline import OfflineProcessor
from app.daily import DailySimulator

# -----------------------------
# 1️⃣ Инициализация
# -----------------------------
clock = Clock()
pizzeria = Pizzeria(config_path="config")
pizzeria.clock = clock

# Добавляем начальный инвентарь
pizzeria.add_initial_inventory()

# -----------------------------
# 2️⃣ Загрузка состояния (если есть)
# -----------------------------
state_file = "pizzeria_state.json"
state = PizzeriaState(pizzeria)

try:
    state.load(state_file)
    print("Состояние загружено из файла")
except FileNotFoundError:
    print("Файл состояния не найден, стартуем с нуля")

# -----------------------------
# 3️⃣ Оффлайн обработка
# -----------------------------
offline_minutes = 60 * 24  # например, прошло 1 день
offline_processor = OfflineProcessor(pizzeria)
offline_processor.apply_offline(offline_minutes)
print(f"Оффлайн обработка: {offline_minutes} минут")

# -----------------------------
# 4️⃣ Создаём тестовые заказы
# -----------------------------
class Order:
    def __init__(self, recipe):
        self.recipe = recipe

# Для теста возьмём 5 заказов
orders = [Order("margherita"), Order("pepperoni"), Order("margherita"),
          Order("pepperoni"), Order("margherita")]

# -----------------------------
# 5️⃣ Симуляция рабочего дня
# -----------------------------
daily_sim = DailySimulator(pizzeria)
summary = daily_sim.run_day(orders, day_minutes=480)  # 8 часов

print("Сводка по дню:")
print(summary)

# -----------------------------
# 6️⃣ Сохраняем состояние
# -----------------------------
state.save(state_file)
print(f"Состояние сохранено в {state_file}")
