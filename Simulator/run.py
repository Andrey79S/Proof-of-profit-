from domain.inventory import Inventory
from domain.ingredient import Ingredient
from core.clock import Clock

clock = Clock()
inv = Inventory()

inv.add(Ingredient("cheese", 1.0, "kg", expires_at=20))
inv.add(Ingredient("cheese", 0.5, "kg", expires_at=100))

clock.advance(30)
inv.cleanup(clock.now)

print(inv.total("cheese"))  # ожидаем 0.5
