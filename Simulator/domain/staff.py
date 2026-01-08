class Staff:
    def __init__(self, name, skills=None):
        self.name = name
        self.skills = skills or {}

    def skill_level(self, skill_name):
        return self.skills.get(skill_name, 1)  # минимальный уровень 1
