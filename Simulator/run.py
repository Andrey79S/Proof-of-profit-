# run.py — новая многодневная версия с интерактивным вводом

import random
from domain.pizzeria import Pizzeria
from domain.order_pool import OrderPool
from core.clock import Clock
from core.scheduler import Scheduler
from engine.simulator import SimulatorEngine


def generate_orders_for_day(order_pool: OrderPool, pizzeria, day_start_min: int, working_hours: int, avg_orders_per_hour: float):
    total_minutes = working_hours * 60
    variation = random.uniform(0.8, 1.3)
    total_orders = max(1, int(avg_orders_per_hour * working_hours * variation))

    recipes = [r for r in pizzeria.recipes.keys() if r != "dough_recipe"]
    if not recipes:
        print("Нет рецептов пицц!")
        return

    print(f"   → Генерация ~{total_orders} заказов (10:00 – {10 + working_hours}:00)")

    for _ in range(total_orders):
        offset = random.randint(0, total_minutes - 10)
        created_at = day_start_min + offset
        recipe = random.choice(recipes)
        max_wait = random.randint(40, 90)
        order_pool.add_order(recipe, created_at_min=created_at, max_wait=max_wait)


print("🍕 Симулятор пиццерии — Настройка симуляции\n")

try:
    days = int(input("Сколько дней симулировать? (например, 7): ") or "7")
except:
    days = 7
try:
    hours_per_day = int(input("Сколько рабочих часов в день? (например, 11): ") or "11")
except:
    hours_per_day = 11
try:
    avg_orders_per_hour = float(input("Среднее количество заказов в час? (например, 7): ") or "7")
except:
    avg_orders_per_hour = 7.0

print(f"\nЗапуск симуляции на {days} дней × {hours_per_day} ч × ~{avg_orders_per_hour} заказов/ч\n")

pizzeria = Pizzeria(config_path="config")
pizzeria.add_initial_inventory()

total_revenue = total_expenses = total_losses = 0.0
total_done = total_failed = total_total = 0
daily_profits = []

for day in range(1, days + 1):
    print(f"\n{'='*20} ДЕНЬ {day} {'='*20}")

    order_pool = OrderPool()
    pizzeria.order_pool = order_pool

    clock = Clock()
    pizzeria.clock = clock

    scheduler = Scheduler()
    sim = SimulatorEngine(pizzeria, order_pool, clock, scheduler)

    day_start_min = (10 * 60) + (day - 1) * 24 * 60
    generate_orders_for_day(order_pool, pizzeria, day_start_min, hours_per_day, avg_orders_per_hour)

    sim.run(total_minutes=24 * 60 + 120)  # полный день + запас

    day_revenue = pizzeria.revenue - total_revenue
    day_expenses = pizzeria.expenses - total_expenses
    day_losses = sim.stats["losses"] - total_losses
    day_profit = day_revenue - day_expenses - day_losses

    daily_profits.append(day_profit)

    total_revenue = pizzeria.revenue
    total_expenses = pizzeria.expenses
    total_losses = sim.stats["losses"]
    total_total += sim.stats["orders_total"]
    total_done += sim.stats["orders_done"]
    total_failed += sim.stats["orders_failed"]

    print(f"День {day}: {sim.stats['orders_done']} сделано | {sim.stats['orders_failed']} провалено | Прибыль дня: {day_profit:.2f}$")

print("\n" + "="*60)
print("ФИНАЛЬНЫЙ ОТЧЁТ")
print("="*60)
print(f"Выручка: {total_revenue:.2f}$ | Расходы: {total_expenses:.2f}$ | Потери: {total_losses:.2f}$")
print(f"Чистая прибыль: {total_revenue - total_expenses - total_losses:.2f}$ | В день: {(total_revenue - total_expenses - total_losses)/days:.2f}$")
print(f"Заказы: {total_total} | Сделано: {total_done} | Провалено: {total_failed}")
if daily_profits:
    print(f"Лучший день: +{max(daily_profits):.2f}$ | Худший: +{min(daily_profits):.2f}$")
