#persistence/state.py

import json
from domain.pizzeria import Pizzeria

def save_state(pizzeria):
state = {
"time": pizzeria.clock.now(),
"ingredients": pizzeria.inventory.ingredients,
"dough_batches": [
{"amount": b.amount_kg, "prepared": b.prepared_at_min, "expires": b.expires_at_min}
for b in pizzeria.inventory.dough_batches
],
"finance": {
"revenue": pizzeria.finance.revenue,
"expenses": pizzeria.finance.expenses,
"losses": pizzeria.finance.losses
}
}
with open("state.json", "w", encoding="utf-8") as f:
json.dump(state, f, indent=2)
print("Состояние сохранено")

def load_state(loader):
try:
with open("state.json", "r", encoding="utf-8") as f:
data = json.load(f)
pizzeria = Pizzeria(loader)
pizzeria.clock = Clock(data["time"])
pizzeria.inventory.ingredients = data["ingredients"]
pizzeria.finance.revenue = data["finance"]["revenue"]
pizzeria.finance.expenses = data["finance"]["expenses"]
pizzeria.finance.losses = data["finance"]["losses"]
# Восстановление теста
from domain.product import DoughBatch
pizzeria.inventory.dough_batches = [
DoughBatch(b["amount"], b["prepared"], b["expires"])
for b in data["dough_batches"]
]
return pizzeria
except FileNotFoundError:
return None
