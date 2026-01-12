# domain/pizzeria/production.py

class Production:
    """
    Производство пиццерии
    - consume заказы из резерва
    - считает ингредиенты, энергию, доходы
    """

    def __init__(self, reserve, base_capacity: int, cost_per_pizza: float = 2.0, price_per_pizza: float = 5.0, energy_per_pizza: float = 0.2):
        self.reserve = reserve
        self.base_capacity = base_capacity
        self.cost_per_pizza = cost_per_pizza
        self.price_per_pizza = price_per_pizza
        self.energy_per_pizza = energy_per_pizza

        # отчёт
        self.revenue = 0.0
        self.expenses = 0.0
        self.ingredients_used = 0.0
        self.energy_used = 0.0

    def simulate_production(self, hours: int):
        capacity = self.base_capacity * hours
        orders_to_produce = self.reserve.consume_for_production(capacity)
        total_pizzas = sum(orders_to_produce.values())
        self.revenue += total_pizzas * self.price_per_pizza
        self.expenses += total_pizzas * self.cost_per_pizza
        self.ingredients_used += total_pizzas * 0.1  # кг на пиццу
        self.energy_used += total_pizzas * self.energy_per_pizza
        return {
            "produced": total_pizzas,
            "orders_detail": orders_to_produce,
            "revenue": self.revenue,
            "expenses": self.expenses,
            "profit": self.revenue - self.expenses,
            "ingredients_used_kg": self.ingredients_used,
            "energy_used_kwh": self.energy_used
      }
