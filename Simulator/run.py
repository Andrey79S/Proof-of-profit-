# run.py

import random
from domain.pizzeria import Pizzeria
from domain.order_pool import OrderPool
from core.clock import Clock
from core.scheduler import Scheduler
from engine.simulator import SimulatorEngine


def generate_orders_for_day(order_pool: OrderPool, pizzeria, day_start_min: int, working_hours: int, avg_orders_per_hour: float):
    """
    Генерирует заказы на один рабочий день в рабочее время (10:00 – 10:00 + working_hours)
    """
    total_minutes = working_hours * 60
    variation = random.uniform(0.8, 1.3)  # ±30% вариация количества заказов
    total_orders = max(1, int(avg_orders_per_hour * working_hours * variation))

    recipes = list(pizzeria.recipes.keys())
    recipes = [r for r in recipes if r != "dough_batch"]  # исключаем рецепт теста
    if not recipes:
        print("Внимание: нет рецептов пицц!")
        return

    print(f"   → Генерация ~{total_orders} заказов с {day_start_min//60:02d}:00 до {(day_start_min + total_minutes)//60:02d}:00")

    for _ in range(total_orders):
        offset_min = random.randint(0, total_minutes - 10)  # чтобы не в последнюю минуту
        created_at = day_start_min + offset_min
        recipe = random.choice(recipes)
        max_wait = random.randint(40, 90)  # терпение клиента

        order_pool.add_order(recipe, created_at_min=created_at, max_wait=max_wait)


# === Интерактивная настройка симуляции ===
print("🍕 Симулятор пиццерии — Настройка симуляции\n")

try:
    days = int(input("Сколько дней симулировать? (например, 7): ").strip() or "7")
except:
    days = 7
try:
    hours_per_day = int(input("Сколько рабочих часов в день? (например, 11): ").strip() or "11")
except:
    hours_per_day = 11
try:
    avg_orders_per_hour = float(input("Среднее количество заказов в час? (например, 8): ").strip() or "8")
except:
    avg_orders_per_hour = 8.0

print(f"\nЗапуск симуляции: {days} дней × {hours_per_day} ч/день × ~{avg_orders_per_hour} заказов/ч")
print(f"Ожидается примерно {int(avg_orders_per_hour * hours_per_day * days)} заказов\n")

# === Инициализация пиццерии ===
pizzeria = Pizzeria(config_path="config")
pizzeria.add_initial_inventory()

# Накопительные показатели за весь период
total_revenue = 0.0
total_expenses = 0.0
total_losses = 0.0
total_orders_total = 0
total_orders_done = 0
total_orders_failed = 0

daily_profits = []

# === Многодневная симуляция ===
for day in range(1, days + 1):
    print(f"\n{'='*15} ДЕНЬ {day} {'='*15}")

    # Новый пул заказов и часы для каждого дня
    order_pool = OrderPool()
    pizzeria.order_pool = order_pool

    clock = Clock()
    pizzeria.clock = clock

    scheduler = Scheduler()
    sim = SimulatorEngine(pizzeria, order_pool, clock, scheduler)

    # Время начала рабочего дня (10:00)
    day_start_min = (10 * 60) + (day - 1) * 24 * 60

    # Генерация заказов на этот день
    generate_orders_for_day(order_pool, pizzeria, day_start_min, hours_per_day, avg_orders_per_hour)

    # Симуляция одного полного дня (24 часа + запас)
    sim.run(total_minutes=24 * 60 + 60)

    # Сбор статистики за день
    day_revenue = pizzeria.revenue - total_revenue
    day_expenses = pizzeria.expenses - total_expenses
    day_losses = sim.stats["losses"] - total_losses
    day_profit = day_revenue - day_expenses - day_losses

    daily_profits.append(day_profit)

    # Накопление
    total_revenue = pizzeria.revenue
    total_expenses = pizzeria.expenses
    total_losses = sim.stats["losses"]
    total_orders_total += sim.stats["orders_total"]
    total_orders_done += sim.stats["orders_done"]
    total_orders_failed += sim.stats["orders_failed"]

    print(f"День {day}: {sim.stats['orders_done']} приготовлено | {sim.stats['orders_failed']} провалено | Прибыль дня: {day_profit:.2f}$")

# === Финальный отчёт ===
print("\n" + "="*60)
print("ФИНАЛЬНЫЙ ОТЧЁТ ЗА ВЕСЬ ПЕРИОД")
print("="*60)
print(f"Период симуляции:     {days} дней")
print(f"Выручка всего:        {total_revenue:.2f}$")
print(f"Расходы (энергия + закупки): {total_expenses:.2f}$")
print(f"Потери от порчи:      {total_losses:.2f}$")
print(f"Чистая прибыль:       {total_revenue - total_expenses - total_losses:.2f}$")
print(f"Прибыль в день:       {(total_revenue - total_expenses - total_losses) / days:.2f}$\n")

print(f"Заказы всего:         {total_orders_total}")
print(f"Приготовлено:         {total_orders_done} ({total_orders_done/total_orders_total*100:.1f}% при наличии заказов)")
print(f"Провалено:            {total_orders_failed}")

if daily_profits:
    print(f"\nЛучший день:          +{max(daily_profits):.2f}$")
    print(f"Худший день:          +{min(daily_profits):.2f}$")
    print(f"Средняя прибыль/день: {sum(daily_profits)/len(daily_profits):.2f}$")

print("\nСимуляция завершена. Готов к новым тестам! 🍕")
