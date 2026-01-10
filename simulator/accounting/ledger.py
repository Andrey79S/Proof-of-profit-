class Ledger:
    def __init__(self):
        self.revenue = 0.0
        self.expenses = 0.0
        self.ingredients_used = 0.0
        self.energy_used = 0.0
        self.pizza_details = {}  # хранит количество пицц по типам

    def add(self, econ_data: dict):
        self.revenue += econ_data["revenue"]
        self.expenses += econ_data["expenses"]
        self.ingredients_used += econ_data["ingredients_used_kg"]
        self.energy_used += econ_data["energy_used_kwh"]

        # обновляем количество пицц
        for pizza_type, qty in econ_data["details"]["per_pizza_type"].items():
            self.pizza_details[pizza_type] = self.pizza_details.get(pizza_type, 0) + qty

    @property
    def profit(self) -> float:
        return self.revenue - self.expenses
