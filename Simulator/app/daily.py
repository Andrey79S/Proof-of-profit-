#app/daily.py

from domain.order import Order
from engine.production import cook_pizza

def run_daily(pizzeria):
print("Рабочий день начался")

# Пример: 8 часов работы  
for hour in range(8):  
    pizzeria.clock.tick(60)  # 1 час  
    print(f"Час {pizzeria.clock.get_hour()}:00")  

    # Пример заказа  
    order = Order("margarita", pizzeria.clock.now())  
    cook_pizza(pizzeria, order)
