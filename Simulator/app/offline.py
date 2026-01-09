def apply_offline(pizzeria):
    print("Оффлайн-процессы...")
    # Порча, энергия холодильников
    engine.spoilage.apply_spoilage(pizzeria, pizzeria.clock.now())
    engine.energy.calculate_daily_energy(pizzeria)
