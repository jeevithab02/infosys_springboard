from random import randint, uniform, choice
from datetime import datetime, timedelta

from backend.database.connection import SessionLocal, Base, engine

from backend.models.user import User
from backend.models.machine import Machine
from backend.models.telemetry import Telemetry
from backend.models.maintenance import Maintenance
from backend.models.alert import Alert
from backend.models.charging_session import ChargingSession
from backend.models.operator import Operator
from backend.models.failure_history import FailureHistory
from backend.models.prediction import Prediction
from backend.models.feedback import Feedback
from backend.auth import hash_password

# Make sure all tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:

    # ============================================================
    # CLEAR EXISTING SEED DATA
    # ============================================================

    print("Clearing existing data...")

    # Delete child/dependent records first
    db.query(Feedback).delete()
    db.query(Prediction).delete()
    db.query(FailureHistory).delete()
    db.query(Alert).delete()
    db.query(ChargingSession).delete()
    db.query(Maintenance).delete()
    db.query(Telemetry).delete()
    db.query(Operator).delete()
    db.query(User).delete()
    db.query(Machine).delete()

    db.commit()

    print("Existing data cleared.")

    # ============================================================
    # 1. USERS
    # ============================================================

    print("Creating users...")

    users = []

    for i in range(1, 11):
        user = User(
            name=f"User {i}",
            email=f"user{i}@example.com",
            password=hash_password(f"password{i}"),
        )

        users.append(user)

    db.add_all(users)
    db.commit()

    print("10 users created.")
    # ============================================================
    # 2. CHARGING STATIONS
    # ============================================================

    print("Creating charging stations...")

    charger_types = ["AC Level 2", "DC Fast Charger", "CCS", "CHAdeMO", "Type 2"]

    locations = ["Hyderabad", "Visakhapatnam", "Vijayawada", "Bengaluru", "Chennai"]

    stations = []

    for i in range(1, 51):

        station = Machine(
            station_name=f"Charging Station {i}",
            charger_type=choice(charger_types),
            location=choice(locations),
        )

        stations.append(station)

    db.add_all(stations)
    db.commit()

    print("50 charging stations created.")

    # Get actual station IDs
    station_ids = [station.id for station in stations]

    # ============================================================
    # 3. TELEMETRY
    # ============================================================

    print("Creating telemetry data...")

    for _ in range(500):

        station_id = choice(station_ids)

        telemetry = Telemetry(
            charging_station_id=station_id,
            temperature=round(uniform(25, 55), 2),
            humidity=round(uniform(30, 90), 2),
            power_consumption=round(uniform(10, 35), 2),
        )

        db.add(telemetry)

    db.commit()

    print("500 telemetry records created.")

    # ============================================================
    # 4. MAINTENANCE
    # ============================================================

    print("Creating maintenance records...")

    maintenance_statuses = ["Completed", "Pending", "Scheduled"]

    base_date = datetime(2026, 7, 1)

    for i in range(100):

        maintenance = Maintenance(
            charging_station_id=choice(station_ids),
            maintenance_date=base_date + timedelta(days=i % 60),
            status=choice(maintenance_statuses),
        )

        db.add(maintenance)

    db.commit()

    print("100 maintenance records created.")

    # ============================================================
    # 5. ALERTS
    # ============================================================

    print("Creating alert records...")

    alert_types = [
        "High Temperature",
        "High Humidity",
        "High Power Consumption",
        "Voltage Issue",
        "Sensor Failure",
    ]

    descriptions = {
        "High Temperature": "Temperature exceeded the recommended operating limit.",
        "High Humidity": "Humidity level is above the recommended range.",
        "High Power Consumption": "Power consumption is higher than the normal operating range.",
        "Voltage Issue": "Abnormal electrical operating condition detected.",
        "Sensor Failure": "Telemetry sensor is not responding correctly.",
    }

    for _ in range(50):

        alert_type = choice(alert_types)

        alert = Alert(
            charging_station_id=choice(station_ids),
            alert_type=alert_type,
            description=descriptions[alert_type],
            is_resolved=choice([True, False]),
            timestamp=datetime.utcnow(),
        )

        db.add(alert)

    db.commit()

    print("50 alert records created.")

    # ============================================================
    # 6. CHARGING SESSIONS
    # ============================================================

    print("Creating charging session records...")

    base_time = datetime(2026, 8, 1, 8, 0)

    for i in range(200):

        start = base_time + timedelta(minutes=i * 45)

        duration = randint(20, 90)

        end = start + timedelta(minutes=duration)

        session = ChargingSession(
            station_id=choice(station_ids),
            vehicle_id=f"EV{1000 + i}",
            start_time=start,
            end_time=end,
            energy_consumed=round(uniform(10, 60), 2),
            cost=round(uniform(150, 900), 2),
        )

        db.add(session)

    db.commit()

    print("200 charging session records created.")

    # ============================================================
    # 7. OPERATORS
    # ============================================================

    print("Creating operators...")

    operators = [
        Operator(
            name="Rahul Sharma",
            email="rahul@example.com",
            phone="9876543210",
            shift="Morning",
        ),
        Operator(
            name="Priya Nair",
            email="priya@example.com",
            phone="9876543211",
            shift="Evening",
        ),
        Operator(
            name="Arjun Kumar",
            email="arjun@example.com",
            phone="9876543212",
            shift="Night",
        ),
        Operator(
            name="Sneha Reddy",
            email="sneha@example.com",
            phone="9876543213",
            shift="Morning",
        ),
        Operator(
            name="Kiran Patel",
            email="kiran@example.com",
            phone="9876543214",
            shift="Evening",
        ),
    ]

    db.add_all(operators)
    db.commit()

    print("5 operators created.")

    # ============================================================
    # 8. FAILURE HISTORY
    # ============================================================

    print("Creating failure history...")

    failure_types = [
        "Power Failure",
        "Connector Fault",
        "Communication Error",
        "Overheating",
        "Sensor Failure",
    ]

    failure_descriptions = {
        "Power Failure": "Station lost power during charging.",
        "Connector Fault": "Charging connector malfunction detected.",
        "Communication Error": "Unable to communicate with the charging server.",
        "Overheating": "Charging station exceeded safe temperature limits.",
        "Sensor Failure": "Telemetry sensor stopped responding.",
    }

    for i in range(50):

        failure_type = choice(failure_types)

        failure = FailureHistory(
            charging_station_id=choice(station_ids),
            failure_type=failure_type,
            description=failure_descriptions[failure_type],
            failure_date=datetime(2026, 7, 1) + timedelta(days=i),
            resolved=choice(["Yes", "No"]),
        )

        db.add(failure)

    db.commit()

    print("50 failure history records created.")

    # ============================================================
    # 9. PREDICTIONS
    # ============================================================

    print("Creating prediction records...")

    for _ in range(20):

        temperature = round(uniform(25, 55), 2)
        humidity = round(uniform(30, 90), 2)
        power = round(uniform(10, 35), 2)

        # Simple rule matching the type of conditions
        # used by the current ML training approach.
        severe_conditions = 0

        if temperature > 45:
            severe_conditions += 1

        if humidity > 75:
            severe_conditions += 1

        if power > 25:
            severe_conditions += 1

        if severe_conditions >= 2:
            result = "Failure Expected"
        else:
            result = "Charging Station Healthy"

        prediction = Prediction(
            charging_station_id=choice(station_ids),
            temperature=temperature,
            humidity=humidity,
            power_consumption=power,
            prediction=result,
        )

        db.add(prediction)

    db.commit()

    print("20 prediction records created.")

    # ============================================================
    # 10. FEEDBACK
    # ============================================================

    print("Creating feedback records...")

    feedback_comments = [
        "Excellent charging experience.",
        "Charging was fast and reliable.",
        "Station was clean and easy to use.",
        "Charging took longer than expected.",
        "Good overall experience.",
    ]

    for i in range(20):

        feedback = Feedback(
            user_id=users[i % len(users)].id,
            charging_station_id=choice(station_ids),
            comments=choice(feedback_comments),
            rating=randint(3, 5),
        )

        db.add(feedback)

    db.commit()

    print("20 feedback records created.")

    # ============================================================
    # FINAL MESSAGE
    # ============================================================

    print("\n======================================")
    print("DATABASE SEEDING COMPLETED SUCCESSFULLY")
    print("======================================")
    print("Users              : 10")
    print("Charging Stations  : 50")
    print("Telemetry          : 500")
    print("Maintenance        : 100")
    print("Alerts             : 50")
    print("Charging Sessions  : 200")
    print("Operators          : 5")
    print("Failure History    : 50")
    print("Predictions        : 20")
    print("Feedback           : 20")
    print("======================================")


except Exception as e:

    db.rollback()

    print("\nERROR WHILE SEEDING DATABASE:")
    print(e)

    raise

finally:

    db.close()
