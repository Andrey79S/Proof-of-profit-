class Staff:
    def __init__(self, name, skill_level=1):
        self.name = name
        self.skill_level = skill_level
        self.busy = False

    def assign_task(self):
        self.busy = True

    def complete_task(self):
        self.busy = False
