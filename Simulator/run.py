# run.py

import random
from domain.pizzeria import Pizzeria
from domain.order_pool import OrderPool
from core.clock import Clock
from core.scheduler import Scheduler
from engine.simulator import SimulatorEngine


def generate_orders_for_day(order_pool: OrderPool, pizzeria, day_start_min: int, working_hours: int, avg_orders_per_hour: float):
    total_minutes = working_hours * 60
    total_orders = max(1, int(avg_orders_per_hour * working_hours * (0.8 + random.random() * 0.4)))  # ±20% вариация

    recipes = list(pizzeria.recipes.keys())
    if not recipes:
        print("Внимание: нет рецептов!")
        return

    print(f"   → Генерация ~{total_orders} заказов (с {day_start_min//60:02d}:00 до {(day_start_min + total_minutes)//60:02d}:00)")

    for _ in range(total_orders):
        offset_min = random.randint(0, total_minutes - 1)
        created_at = day_start_min + offset_min
        recipe = random.choice(recipes)
        max_wait = random.randint(40, 90)
        order_pool.add_order(recipe, created_at_min=created_at, max_wait=max_wait)


# === Настройка симуляции ===
print("🍕 Симулятор пиццерии — Настройка симуляции\n")

try:
    days = int(input("Сколько дней симулировать? (например, 7): "))
except:
    days = 7
try:
    hours_per_day = int(input("Сколько рабочих часов в день? (например, 8): "))
except:
    hours_per_day = 8
try:
    avg_orders_per_hour = float(input("Среднее количество заказов в час? (например, 5.5): "))
except:
    avg_orders_per_hour = 5.0

# === Инициализация ===
print("\nЗагрузка пиццерии...")
pizzeria = Pizzeria(config_path="config")
pizzeria.add_initial_inventory()

# Накопительные переменные
total_revenue = 0.0
total_expenses = 0.0
total_losses = 0.0
total_orders_processed = 0
total_orders_failed = 0
total_orders_total = 0

daily_profits = []

print(f"\nЗапуск симуляции: {days} дней × {hours_per_day} ч = ~{avg_orders_per_hour * hours_per_day * days:.0f} заказов\n")

for day in range(1, days + 1):
    print(f"{'='*10} ДЕНЬ {day} {'='*10}")

    # Новый пул заказов и clock для каждого дня
    order_pool = OrderPool()
    pizzeria.order_pool = order_pool

    clock = Clock()
    pizzeria.clock = clock

    scheduler = Scheduler()
    sim = SimulatorEngine(pizzeria, order_pool, clock, scheduler)

    # Правильное время начала рабочего дня (10:00 каждого календарного дня)
    day_start_min = (10 * 60) + (day - 1) * 24 * 60

    # Генерация заказов на этот день
    generate_orders_for_day(order_pool, pizzeria, day_start_min, hours_per_day, avg_orders_per_hour)

    # Симуляция одного дня (немного больше, чтобы всё успело приготовиться)
    sim.run(total_minutes=hours_per_day * 60 + 60)

    # Сбор статистики за день
    day_revenue = pizzeria.revenue - total_revenue  # прирост
    day_expenses = pizzeria.expenses - total_expenses
    day_losses = sim.stats["losses"] - total_losses

    day_profit = day_revenue - day_expenses - (sim.stats["losses"] - total_losses)

    daily_profits.append(day_profit)

    # Накопление
    total_revenue = pizzeria.revenue
    total_expenses = pizzeria.expenses
    total_losses = sim.stats["losses"]
    total_orders_processed += sim.stats["orders_done"]
    total_orders_failed += sim.stats["orders_failed"]
    total_orders_total += sim.stats["orders_total"]

    print(f"День {day}: {sim.stats['orders_done']} сделано, "
          f"{sim.stats['orders_failed']} провалено, "
          f"прибыль дня: {day_profit:.2f}$")

# === Финальный отчёт ===
print("\n" + "="*60)
print("ФИНАЛЬНЫЙ ОТЧЁТ ЗА ВСЮ СИМУЛЯЦИЮ")
print("="*60)
print(f"Период:               {days} дней")
print(f"Выручка:              {total_revenue:.2f}$")
print(f"Расходы (энергия):    {total_expenses - total_losses:.2f}$")
print(f"Потери (порча):       {total_losses:.2f}$")
print(f"Чистая прибыль:       {total_revenue - total_expenses:.2f}$")
print(f"Прибыль в день:       {(total_revenue - total_expenses) / days:.2f}$\n")

print(f"Заказы всего:         {total_orders_total}")
print(f"Обработано:           {total_orders_processed} ({total_orders_processed/total_orders_total*100:.1f}%)")
print(f"Провалено:            {total_orders_failed}")

if daily_profits:
    print(f"\nЛучший день:          +{max(daily_profits):.2f}$")
    print(f"Худший день:          +{min(daily_profits):.2f}$")
