# engine/production.py

class ProductionEngine:
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria  # Не импортируем класс, а принимаем готовый объект

    def make_dough(self, amount_kg: float, now: int):
        mixer = next((eq for eq in self.pizzeria.equipment.values() if eq.type == "mixer"), None)
        if not mixer or not mixer.can_use(amount_kg):
            return False

        # Предположим, что время замеса пропорционально объёму
        mix_time = 10 + (amount_kg / 5) * 5  # пример
        # Здесь в реальной симуляции нужно тикать clock на mix_time

        lifetime = 1440  # 24 часа, можно взять из конфига
        from domain.product import DoughBatch  # Локальный импорт внутри метода — безопасно
        batch = DoughBatch(amount_kg, now, now + lifetime)
        self.pizzeria.inventory.add_dough_batch(batch)

        # Энергия за замес
        self.pizzeria.energy_consumed += mixer.power_kw * (mix_time / 60)
        return True
