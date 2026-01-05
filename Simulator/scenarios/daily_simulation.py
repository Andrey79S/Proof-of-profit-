for minute in range(day_minutes):
    scheduler.tick()
    available_orders = order_pool.get_available(scheduler.now)
    for order in available_orders:
        for pizzeria in pizzerias:
            if pizzeria.accept_order(order, scheduler.now):
                break  # заказ принят одной пиццерией
    order_pool.expire_orders(scheduler.now)
