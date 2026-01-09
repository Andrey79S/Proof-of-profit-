# engine/spoilage.py

class SpoilageEngine:
    """
    Рассчитывает порчу ингредиентов и теста
    """
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria

    def spoil_ingredients(self):
        """
        Проверяет ингредиенты и тесто на порчу.
        Уменьшает количество испорченных единиц и увеличивает потери.
        """
        now = self.pizzeria.clock.now() if self.pizzeria.clock else 0

        # --- Порча ингредиентов ---
        for ing_dict in [self.pizzeria.inventory.ingredients, self.pizzeria.inventory.table_ingredients]:
            for ing in ing_dict.values():
                # Простая модель: если ingredient хранится > 7 дней (10080 мин), портится 10%
                if hasattr(ing, 'stored_at_min'):
                    if now - ing.stored_at_min > 10080:  # 7 дней
                        loss = ing.amount_kg * 0.1
                        ing.amount_kg -= loss
                        self.pizzeria.losses += loss

        # --- Порча теста ---
        for batch_list in [self.pizzeria.inventory.dough_batches, self.pizzeria.inventory.table_dough]:
            for batch in batch_list[:]:
                if batch.is_expired(now):
                    self.pizzeria.losses += batch.amount_kg
                    batch_list.remove(batch)
