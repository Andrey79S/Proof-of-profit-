class DoughMixer:
    def __init__(self, power_kw, time_min, max_load):
        self.power_kw = power_kw          # кВт
        self.time_min = time_min          # минут на замес
        self.max_load = max_load          # кг теста за раз

    def mix(self, dough_kg):
        """
        Возвращает:
        - затраченную энергию (кВт·ч)
        - количество замесов
        """
        batches = -(-dough_kg // self.max_load)  # ceil без math
        total_time_hours = batches * (self.time_min / 60)

        energy_used = self.power_kw * total_time_hours

        return {
            "batches": int(batches),
            "energy_kwh": energy_used,
            "time_hours": total_time_hours
        }
