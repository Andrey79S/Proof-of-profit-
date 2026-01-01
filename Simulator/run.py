# simulator/run.py

from engine.pizzeria import Pizzeria
from work_session import WorkSession

if __name__ == "__main__":
    pizzeria = Pizzeria()
    session = WorkSession(pizzeria, duration_minutes=720)  # 12 часов
    report = session.run()

    print("📊 Session report:")
    for k,v in report.items():
        print(f"{k}: {v}")
