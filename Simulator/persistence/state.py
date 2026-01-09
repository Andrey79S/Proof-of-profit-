import json

def save_state(pizzeria):
    state = {
        "inventory": pizzeria.inventory.ingredients,
        "finance": pizzeria.finance,
        "last_time": pizzeria.clock.now()
    }
    with open("state.json", "w") as f:
        json.dump(state, f)

def load_state(loader):
    try:
        with open("state.json", "r") as f:
            data = json.load(f)
        pizzeria = Pizzeria(loader)
        pizzeria.inventory.ingredients = data["inventory"]
        pizzeria.finance = data["finance"]
        pizzeria.clock = Clock(data["last_time"])
        return pizzeria
    except FileNotFoundError:
        return None
