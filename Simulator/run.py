from domain.recipe import Recipe
from domain.kitchen import Kitchen

pizza = Recipe("Margherita", {
    "cheese": 0.2,
    "flour": 0.3
})

kitchen = Kitchen(inv)

print(kitchen.can_cook(pizza))  # True
kitchen.cook(pizza)
print(inv.total("cheese"))      # 0.3
