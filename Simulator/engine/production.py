from domain.dough import Dough
from domain.inventory import Inventory
from domain.equipment import DoughMixer

class Production:
    def __init__(self, inventory: Inventory, mixer: DoughMixer):
        self.inventory = inventory
        self.mixer = mixer
        self.dough_storage = Dough()

    def mix_dough_if_needed(self, amount_needed: float):
        if self.dough_storage.weight < amount_needed:
            # Проверяем ингредиенты
            flour_needed = amount_needed * 0.6
            water_needed = amount_needed * 0.33
            yeast_needed = amount_needed * 0.04
            salt_needed = amount_needed * 0.005
            oil_needed = amount_needed * 0.025

            if self.inventory.has_ingredients(flour=flour_needed, water=water_needed,
                                              yeast=yeast_needed, salt=salt_needed,
                                              olive_oil=oil_needed):
                self.inventory.remove(flour=flour_needed, water=water_needed,
                                      yeast=yeast_needed, salt=salt_needed,
                                      olive_oil=oil_needed)
                dough_made = self.mixer.mix(amount_needed)
                self.dough_storage.add(dough_made)
                print(f"[Production] Замесов: 1, Произведено теста: {dough_made:.2f} кг")
            else:
                print("[Production] Недостаточно ингредиентов для замеса теста")
