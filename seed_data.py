from random import randint, uniform, choice

from backend.database.connection import SessionLocal
from backend.models.machine import Machine
from backend.models.telemetry import Telemetry
from backend.models.maintenance import Maintenance
from backend.models.prediction import Prediction
from backend.models.feedback import Feedback

db = SessionLocal()

# -----------------------
# Create Charging Stations
# -----------------------

charger_types = [
    "AC Level 2",
    "DC Fast Charger",
    "CCS",
    "CHAdeMO",
    "Type 2"
]

locations = [
    "Hyderabad",
    "Visakhapatnam",
    "Vijayawada",
    "Bengaluru",
    "Chennai"
]

print("Creating charging stations...")

for i in range(1, 51):
    charging_station = Machine(
        station_name=f"Charging Station {i}",
        charger_type=choice(charger_types),
        location=choice(locations)
    )

    db.add(charging_station)

db.commit()

print("50 charging stations created.")

# -----------------------
# Create 500 Telemetry Records
# -----------------------

print("Creating telemetry data...")

for _ in range(500):

    telemetry = Telemetry(
        charging_station_id=randint(1, 50),
        temperature=round(uniform(25, 45), 2),
        humidity=round(uniform(30, 60), 2),
        power_consumption=round(uniform(10, 30), 2)
    )

    db.add(telemetry)

db.commit()

print("500 telemetry records created.")

# -----------------------
# Create 100 Maintenance Records
# -----------------------

statuses = [
    "Completed",
    "Pending",
    "Scheduled"
]

print("Creating maintenance records...")

for i in range(100):

    maintenance = Maintenance(
        charging_station_id=randint(1, 50),
        maintenance_date=f"2026-07-{(i % 30) + 1:02d}",
        status=choice(statuses)
    )

    db.add(maintenance)

db.commit()

print("100 maintenance records created.")

db.close()

print("\nDatabase populated successfully.")

for _ in range(20):

    prediction = Prediction(
        temperature=30,
        humidity=45,
        power_consumption=12,
        prediction="Charging Station Healthy"
    )

    db.add(prediction)

for i in range(10):

    feedback = Feedback(
        user_name=f"User {i}",
        comments="Excellent Service",
        rating=5
    )

    db.add(feedback)

db.commit()
db.close()

print("20 predictions and 10 feedback added.")