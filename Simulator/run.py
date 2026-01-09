from core.clock import Clock

clock = Clock()
print(clock.now())   # 0
clock.tick(15)
print(clock.now())   # 15
