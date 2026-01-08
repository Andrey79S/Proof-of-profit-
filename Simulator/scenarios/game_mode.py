# Простой режим для TG: "Тапы" добавляют заказы
from scenarios.daily_simulation import simulate_day

def game_mode(pizzeria, taps: int):
    # Каждый тап добавляет заказ
    for _ in range(taps):
        pizzeria.order_pool.add_order("margarita", pizzeria.clock.now(), 30)
    simulate_day(pizzeria, pizzeria.order_pool)
    # Для TG: Вернуть stats
