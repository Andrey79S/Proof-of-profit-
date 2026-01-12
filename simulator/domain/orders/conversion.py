# domain/orders/conversion.py
import random

def convert_orders_to_pizzas(amount: int, menu_level: int) -> dict:
    """
    При резервировании:
    - превращаем «абстрактные заказы» в конкретные пиццы
    - menu_level = влияет на % премиум-пицц
    """
    if amount <= 0:
        return {}

    basic = int(amount * 0.7)
    premium = int(amount * 0.3 * menu_level / 1)
    return {
        "basic": basic,
        "premium": premium
    }
