# engine/energy.py

class EnergyEngine:
    """
    Подсчёт энергопотребления пиццерии
    """
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria

    def daily_fridge_consumption(self):
        """
        Круглосуточная работа холодильников
        """
        fridge_power = sum(
            eq.power_kw for eq in self.pizzeria.equipment.values()
            if eq.type in ["fridge", "proofing_fridge", "table_fridge"]
        )
        daily_kwh = fridge_power * 24
        daily_cost = daily_kwh * self.pizzeria.economy.get("electricity_price_per_kwh", 0.2)

        self.pizzeria.energy_consumed += daily_kwh
        self.pizzeria.expenses += daily_cost

        return daily_kwh, daily_cost
