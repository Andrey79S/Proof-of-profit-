class Pizzeria:
    def __init__(self, name, inventory, equipment, staff):
        self.name = name
        self.inventory = inventory
        self.equipment = equipment
        self.staff = staff
        self.active_orders: list[Order] = []

    def can_make(self, order: Order) -> bool:
        """Проверка: есть ли ресурсы и свободное оборудование"""
        recipe = order.recipe
        return self.inventory.has_ingredients(recipe) and self.equipment.has_free_slot(recipe)

    def accept_order(self, order: Order, now: int):
        if not self.can_make(order):
            return False
        order.status = OrderStatus.ACCEPTED
        order.accepted_at = now
        self.active_orders.append(order)
        self.start_cooking(order, now)
        return True

    def start_cooking(self, order: Order, now: int):
        order.status = OrderStatus.COOKING
        cooking_time = self.equipment.get_cooking_time(order.recipe)
        # Запланируем завершение через scheduler
        scheduler.schedule(now + cooking_time, lambda: self.finish_order(order))

    def finish_order(self, order: Order):
        order.status = OrderStatus.DONE
        order.completed_at = scheduler.now
        self.active_orders.remove(order)
        self.inventory.consume(order.recipe)
