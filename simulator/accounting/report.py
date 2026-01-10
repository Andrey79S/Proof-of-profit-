def generate_report(pizzeria) -> str:
    ledger = pizzeria.ledger
    menu = pizzeria.menu
    reserve = pizzeria.reserve

    lines = []
    lines.append(f"📊 Pizzeria Report — День {pizzeria.day if hasattr(pizzeria,'day') else 0}\n")

    lines.append("🍕 Пиццы произведены:")
    for pizza_type, qty in ledger.pizza_details.items():
        price = menu.types[pizza_type]["price"]
        lines.append(f"  - {pizza_type.capitalize()}: {qty} x ${price} = ${qty * price}")

    lines.append(f"\n💰 Доход: ${ledger.revenue:.2f}")

    lines.append("\n🥬 Расход ингредиентов:")
    for pizza_type, qty in ledger.pizza_details.items():
        ing_kg = menu.types[pizza_type]["ingredient_kg"]
        cost_per_kg = menu.types[pizza_type].get("ingredient_price_per_kg", 13)
        lines.append(f"  - {qty * ing_kg:.1f} кг x ${cost_per_kg}/кг = ${qty * ing_kg * cost_per_kg:.2f}")

    lines.append("⚡ Расход энергии:")
    for pizza_type, qty in ledger.pizza_details.items():
        kwh = menu.types[pizza_type]["energy_kwh"]
        cost_per_kwh = menu.types[pizza_type].get("energy_price_per_kwh", 1.25)
        lines.append(f"  - {qty * kwh:.1f} kWh x ${cost_per_kwh} = ${qty * kwh * cost_per_kwh:.2f}")

    lines.append(f"\n💵 Общие расходы: ${ledger.expenses:.2f}")
    lines.append(f"💸 Прибыль: ${ledger.profit:.2f}\n")

    lines.append("📈 Апгрейды:")
    upgrades = ["tap_level", "reserve_level", "capacity_level", "efficiency_level", "equipment_level", "staff_level"]
    for u in upgrades:
        lines.append(f"  - {u.replace('_level','').capitalize()}: {getattr(pizzeria,u)}")

    lines.append(f"\n📊 Резерв заказов: {reserve.current}/{pizzeria.max_reserve()}")

    return "\n".join(lines)
