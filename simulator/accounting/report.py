def generate_report(pizzeria):
    return {
        "reserve_left": pizzeria.reserve.current,
        "revenue": pizzeria.ledger.revenue,
        "expenses": pizzeria.ledger.expenses,
        "profit": pizzeria.ledger.profit,
        "ingredients_used_kg": pizzeria.ledger.ingredients_used,
        "energy_used_kwh": pizzeria.ledger.energy_used,
        "menu_level": pizzeria.menu.menu_level,
        "apgrades": {
            "tap_level": pizzeria.tap_level,
            "reserve_level": pizzeria.reserve_level,
            "capacity_level": pizzeria.capacity_level,
            "efficiency_level": pizzeria.efficiency_level,
            "equipment_level": pizzeria.equipment_level,
            "staff_level": pizzeria.staff_level,
        }
    }
