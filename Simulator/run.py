from core.clock import Clock
from domain.order import Order
from domain.order_pool import OrderPool

clock = Clock()
pool = OrderPool()

pool.add(Order("margarita", clock.now, max_wait=30))
pool.add(Order("pepperoni", clock.now, max_wait=5))

clock.advance(10)
pool.expire_orders(clock.now)

print(pool.stats())
print(pool.get_available(clock.now))
