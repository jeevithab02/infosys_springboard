from backend.models import machine

# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException
from backend.database.connection import engine, Base
from backend.models.user import User
from backend.models.machine import Machine
from backend.models.telemetry import Telemetry

# pyrefly: ignore [missing-import]


# pyrefly: ignore [missing-import]
from fastapi import Depends

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from backend.models.maintenance import Maintenance

# pyrefly: ignore [missing-import]


from backend.database.connection import get_db

from backend.ml.predict import predict_failure


from backend.models.operator import Operator


from backend.models.prediction import Prediction


from backend.models.feedback import Feedback


from backend.models.failure_history import FailureHistory


from backend.models.alert import Alert


from backend.models.charging_session import ChargingSession

from backend.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
)

from backend.schemas.machine import (
    MachineCreate,
    MachineUpdate,
    MachineResponse,
)

from backend.schemas.telemetry import (
    TelemetryCreate,
    TelemetryUpdate,
    TelemetryResponse,
)

from backend.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceUpdate,
    MaintenanceResponse,
)

from backend.schemas.alert import (
    AlertCreate,
    AlertUpdate,
    AlertResponse,
)

from backend.schemas.charging_session import (
    ChargingSessionCreate,
    ChargingSessionUpdate,
    ChargingSessionResponse,
)

from backend.schemas.operator import (
    OperatorCreate,
    OperatorUpdate,
    OperatorResponse,
)

from backend.schemas.failure_history import (
    FailureHistoryCreate,
    FailureHistoryUpdate,
    FailureHistoryResponse,
)

from backend.schemas.prediction import (
    PredictionCreate,
    PredictionResponse,
)

from backend.schemas.feedback import (
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackResponse,
)

from backend.schemas.health import StationHealthResponse

from backend.schemas.predict import PredictionInput

from backend.schemas.dashboard import DashboardSummaryResponse

from backend.schemas.analytics import StationAnalyticsResponse

from backend.schemas.login import LoginRequest, LoginResponse

from backend.auth import hash_password, verify_password

tags_metadata = [
    {"name": "System", "description": "API health and system status."},
    {"name": "Users", "description": "User registration and user management."},
    {
        "name": "Charging Stations",
        "description": "Create and manage EV charging stations.",
    },
    {
        "name": "Telemetry",
        "description": "Monitor temperature, humidity and power consumption.",
    },
    {
        "name": "Maintenance",
        "description": "Manage charging station maintenance records.",
    },
    {"name": "Alerts", "description": "Monitor and manage charging station alerts."},
    {"name": "Charging Sessions", "description": "Manage EV charging session records."},
    {"name": "Operators", "description": "Manage charging station operators."},
    {
        "name": "Failure History",
        "description": "Track previous charging station failures.",
    },
    {
        "name": "Predictions",
        "description": "Predict charging station health using the ML model.",
    },
    {
        "name": "Feedback",
        "description": "Manage user feedback and charging station ratings.",
    },
]

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EV Charging Station Health Monitoring API",
    description="""
## EV Charging Station Health Monitoring Backend

REST API for monitoring and managing EV charging stations.

### Main modules

- 👤 User Management
- ⚡ Charging Station Management
- 📊 Telemetry Monitoring
- 🔧 Maintenance Tracking
- 🚨 Alert Management
- 🔋 Charging Sessions
- 👷 Operator Management
- ⚠️ Failure History
- 🤖 ML-based Health Prediction
- ⭐ User Feedback
""",
    version="1.0",
    openapi_tags=tags_metadata,
)


@app.get("/", tags=["System"], summary="Check API status")
def home():
    return {"message": "EV Charging Station Health Monitoring Backend Running"}


@app.post(
    "/users", tags=["Users"], summary="Create a user", response_model=UserResponse
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        name=user.name, email=user.email, password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get(
    "/users/all",
    tags=["Users"],
    summary="Get all users",
    response_model=list[UserResponse],
)
def get_all_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return users


@app.get("/users", tags=["Users"], summary="Check user API")
def get_users():
    return {"message": "User API is working"}


@app.get(
    "/users/{user_id}",
    tags=["Users"],
    summary="Get a user by ID",
    response_model=UserResponse,
)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.put(
    "/users/{user_id}",
    tags=["Users"],
    summary="Update a user",
    response_model=UserResponse,
)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user fields if they are provided
    if user_data.name is not None:
        user.name = user_data.name

    if user_data.email is not None:
        user.email = user_data.email

    if user_data.password is not None:
        user.password = user_data.password

    db.commit()
    db.refresh(user)

    return user


@app.delete("/users/{user_id}", tags=["Users"], summary="Delete a user")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


@app.post(
    "/login",
    tags=["Authentication"],
    summary="Login user",
    response_model=LoginResponse,
)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
    }


@app.post(
    "/charging-stations",
    tags=["Charging Stations"],
    summary="Create a charging station",
    response_model=MachineResponse,
)
def create_charging_station(machine_data: MachineCreate, db: Session = Depends(get_db)):

    charging_station = Machine(
        station_name=machine_data.station_name,
        charger_type=machine_data.charger_type,
        location=machine_data.location,
    )

    db.add(charging_station)
    db.commit()
    db.refresh(charging_station)

    return charging_station


@app.get(
    "/charging-stations/all",
    tags=["Charging Stations"],
    summary="Get all charging stations",
    response_model=list[MachineResponse],
)
def get_all_charging_stations(db: Session = Depends(get_db)):

    charging_stations = db.query(Machine).all()

    return charging_stations


@app.get(
    "/charging-stations",
    tags=["Charging Stations"],
    summary="Check charging station API",
)
def get_charging_stations():
    return {"message": "Charging station API is working"}


@app.get(
    "/charging-stations/{station_id}",
    tags=["Charging Stations"],
    summary="Get a charging station by ID",
    response_model=MachineResponse,
)
def get_charging_station(station_id: int, db: Session = Depends(get_db)):
    station = db.query(Machine).filter(Machine.id == station_id).first()

    if not station:
        raise HTTPException(status_code=404, detail="Charging station not found")

    return station


@app.put(
    "/charging-stations/{station_id}",
    tags=["Charging Stations"],
    summary="Update a charging station",
    response_model=MachineResponse,
)
def update_charging_station(
    station_id: int, station_data: MachineUpdate, db: Session = Depends(get_db)
):
    station = db.query(Machine).filter(Machine.id == station_id).first()

    if not station:
        raise HTTPException(status_code=404, detail="Charging station not found")

    if station_data.station_name is not None:
        station.station_name = station_data.station_name

    if station_data.charger_type is not None:
        station.charger_type = station_data.charger_type

    if station_data.location is not None:
        station.location = station_data.location

    db.commit()
    db.refresh(station)

    return station


@app.delete(
    "/charging-stations/{station_id}",
    tags=["Charging Stations"],
    summary="Delete a charging station",
)
def delete_charging_station(station_id: int, db: Session = Depends(get_db)):
    station = db.query(Machine).filter(Machine.id == station_id).first()

    if not station:
        raise HTTPException(status_code=404, detail="Charging station not found")

    db.delete(station)
    db.commit()

    return {"message": "Charging station deleted successfully"}


@app.get(
    "/charging-stations/{station_id}/health",
    tags=["Charging Stations"],
    summary="Get charging station health summary",
    response_model=StationHealthResponse,
)
def get_station_health(station_id: int, db: Session = Depends(get_db)):
    station = db.query(Machine).filter(Machine.id == station_id).first()

    if not station:
        raise HTTPException(status_code=404, detail="Charging station not found")

    # Get latest telemetry
    latest_telemetry = (
        db.query(Telemetry)
        .filter(Telemetry.charging_station_id == station_id)
        .order_by(Telemetry.id.desc())
        .first()
    )

    # Count unresolved alerts
    active_alerts = (
        db.query(Alert)
        .filter(Alert.charging_station_id == station_id, Alert.is_resolved == False)
        .count()
    )

    # Count failure history
    recent_failures = (
        db.query(FailureHistory)
        .filter(FailureHistory.charging_station_id == station_id)
        .count()
    )

    # Get latest maintenance record
    latest_maintenance = (
        db.query(Maintenance)
        .filter(Maintenance.charging_station_id == station_id)
        .order_by(Maintenance.id.desc())
        .first()
    )

    temperature = None
    humidity = None
    power_consumption = None

    if latest_telemetry:
        temperature = latest_telemetry.temperature
        humidity = latest_telemetry.humidity
        power_consumption = latest_telemetry.power_consumption

    maintenance_status = None

    if latest_maintenance:
        maintenance_status = latest_maintenance.status

    # -------------------------
    # Health calculation
    # -------------------------

    health = "Healthy"

    if temperature is not None and temperature > 45:
        health = "At Risk"

    if humidity is not None and humidity > 75:
        health = "At Risk"

    if power_consumption is not None and power_consumption > 25:
        health = "At Risk"

    if active_alerts >= 2:
        health = "Critical"

    if recent_failures >= 3:
        health = "Critical"

    return {
        "station_id": station.id,
        "station_name": station.station_name,
        "temperature": temperature,
        "humidity": humidity,
        "power_consumption": power_consumption,
        "active_alerts": active_alerts,
        "recent_failures": recent_failures,
        "maintenance_status": maintenance_status,
        "health": health,
    }


@app.get(
    "/charging-stations/{station_id}/analytics",
    tags=["Charging Stations"],
    summary="Get charging station analytics",
    response_model=StationAnalyticsResponse,
)
def get_station_analytics(station_id: int, db: Session = Depends(get_db)):
    # Check station exists
    station = db.query(Machine).filter(Machine.id == station_id).first()

    if not station:
        raise HTTPException(status_code=404, detail="Charging station not found")

    # -------------------------
    # Telemetry statistics
    # -------------------------

    telemetry_records = (
        db.query(Telemetry).filter(Telemetry.charging_station_id == station_id).all()
    )

    if telemetry_records:
        average_temperature = sum(
            record.temperature for record in telemetry_records
        ) / len(telemetry_records)

        average_humidity = sum(record.humidity for record in telemetry_records) / len(
            telemetry_records
        )

        average_power_consumption = sum(
            record.power_consumption for record in telemetry_records
        ) / len(telemetry_records)
    else:
        average_temperature = None
        average_humidity = None
        average_power_consumption = None

    # -------------------------
    # Charging session statistics
    # -------------------------

    sessions = (
        db.query(ChargingSession).filter(ChargingSession.station_id == station_id).all()
    )

    total_energy_consumed = sum(session.energy_consumed or 0 for session in sessions)

    total_charging_cost = sum(session.cost or 0 for session in sessions)

    total_charging_sessions = len(sessions)

    # -------------------------
    # Alert statistics
    # -------------------------

    total_alerts = (
        db.query(Alert).filter(Alert.charging_station_id == station_id).count()
    )

    unresolved_alerts = (
        db.query(Alert)
        .filter(Alert.charging_station_id == station_id, Alert.is_resolved == False)
        .count()
    )

    # -------------------------
    # Failure statistics
    # -------------------------

    total_failures = (
        db.query(FailureHistory)
        .filter(FailureHistory.charging_station_id == station_id)
        .count()
    )

    unresolved_failures = (
        db.query(FailureHistory)
        .filter(
            FailureHistory.charging_station_id == station_id,
            FailureHistory.resolved == "No",
        )
        .count()
    )

    # -------------------------
    # Maintenance statistics
    # -------------------------

    total_maintenance = (
        db.query(Maintenance)
        .filter(Maintenance.charging_station_id == station_id)
        .count()
    )

    return {
        "station_id": station.id,
        "station_name": station.station_name,
        "average_temperature": (
            round(average_temperature, 2) if average_temperature is not None else None
        ),
        "average_humidity": (
            round(average_humidity, 2) if average_humidity is not None else None
        ),
        "average_power_consumption": (
            round(average_power_consumption, 2)
            if average_power_consumption is not None
            else None
        ),
        "total_energy_consumed": round(total_energy_consumed, 2),
        "total_charging_cost": round(total_charging_cost, 2),
        "total_charging_sessions": total_charging_sessions,
        "total_alerts": total_alerts,
        "unresolved_alerts": unresolved_alerts,
        "total_failures": total_failures,
        "unresolved_failures": unresolved_failures,
        "total_maintenance": total_maintenance,
    }


@app.post(
    "/telemetry",
    tags=["Telemetry"],
    summary="Create telemetry record",
    response_model=TelemetryResponse,
)
def create_telemetry(telemetry_data: TelemetryCreate, db: Session = Depends(get_db)):

    telemetry = Telemetry(
        charging_station_id=telemetry_data.charging_station_id,
        temperature=telemetry_data.temperature,
        humidity=telemetry_data.humidity,
        power_consumption=telemetry_data.power_consumption,
    )

    db.add(telemetry)
    db.commit()
    db.refresh(telemetry)

    return telemetry


@app.get("/telemetry/all", tags=["Telemetry"], summary="Get all telemetry records")
def get_all_telemetry(db: Session = Depends(get_db)):

    telemetry = db.query(Telemetry).all()

    return telemetry


@app.get(
    "/telemetry",
    tags=["Telemetry"],
    summary="Check telemetry API",
    response_model=list[TelemetryResponse],
)
def get_telemetry():
    return {"message": "Telemetry API is working"}


@app.get(
    "/telemetry/{telemetry_id}",
    tags=["Telemetry"],
    summary="Get telemetry by ID",
    response_model=TelemetryResponse,
)
def get_telemetry_by_id(telemetry_id: int, db: Session = Depends(get_db)):
    telemetry = db.query(Telemetry).filter(Telemetry.id == telemetry_id).first()

    if not telemetry:
        raise HTTPException(status_code=404, detail="Telemetry record not found")

    return telemetry


@app.put(
    "/telemetry/{telemetry_id}",
    tags=["Telemetry"],
    summary="Update telemetry",
    response_model=TelemetryResponse,
)
def update_telemetry(
    telemetry_id: int, telemetry_data: TelemetryUpdate, db: Session = Depends(get_db)
):
    telemetry = db.query(Telemetry).filter(Telemetry.id == telemetry_id).first()

    if not telemetry:
        raise HTTPException(status_code=404, detail="Telemetry record not found")

    if telemetry_data.temperature is not None:
        telemetry.temperature = telemetry_data.temperature

    if telemetry_data.humidity is not None:
        telemetry.humidity = telemetry_data.humidity

    if telemetry_data.power_consumption is not None:
        telemetry.power_consumption = telemetry_data.power_consumption

    db.commit()
    db.refresh(telemetry)

    return telemetry


@app.delete(
    "/telemetry/{telemetry_id}",
    tags=["Telemetry"],
    summary="Delete telemetry",
)
def delete_telemetry(telemetry_id: int, db: Session = Depends(get_db)):
    telemetry = db.query(Telemetry).filter(Telemetry.id == telemetry_id).first()

    if not telemetry:
        raise HTTPException(status_code=404, detail="Telemetry record not found")

    db.delete(telemetry)
    db.commit()

    return {"message": "Telemetry record deleted successfully"}


@app.post(
    "/maintenance",
    tags=["Maintenance"],
    summary="Create maintenance record",
    response_model=MaintenanceResponse,
)
def create_maintenance(data: MaintenanceCreate, db: Session = Depends(get_db)):

    maintenance = Maintenance(
        charging_station_id=data.charging_station_id,
        maintenance_date=data.maintenance_date,
        status=data.status,
    )

    db.add(maintenance)
    db.commit()
    db.refresh(maintenance)

    return {"message": "Maintenance record added successfully", "id": maintenance.id}


@app.get(
    "/maintenance/all",
    tags=["Maintenance"],
    summary="Get all maintenance records",
    response_model=list[MaintenanceResponse],
)
def get_all_maintenance(db: Session = Depends(get_db)):

    maintenance = db.query(Maintenance).all()

    return maintenance


@app.get(
    "/maintenance/{maintenance_id}",
    tags=["Maintenance"],
    summary="Get maintenance record by ID",
    response_model=MaintenanceResponse,
)
def get_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()

    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    return maintenance


@app.put(
    "/maintenance/{maintenance_id}",
    tags=["Maintenance"],
    summary="Update maintenance record",
    response_model=MaintenanceResponse,
)
def update_maintenance(
    maintenance_id: int,
    maintenance_data: MaintenanceUpdate,
    db: Session = Depends(get_db),
):
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()

    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    if maintenance_data.maintenance_date is not None:
        maintenance.maintenance_date = maintenance_data.maintenance_date

    if maintenance_data.status is not None:
        maintenance.status = maintenance_data.status

    db.commit()
    db.refresh(maintenance)

    return maintenance


@app.delete(
    "/maintenance/{maintenance_id}",
    tags=["Maintenance"],
    summary="Delete maintenance record",
)
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()

    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    db.delete(maintenance)
    db.commit()

    return {"message": "Maintenance record deleted successfully"}


@app.post(
    "/predict",
    tags=["Predictions"],
    summary="Predict charging station health",
    description="""
Uses the trained machine learning model to predict
whether a charging station is healthy or likely to fail.

The prediction is based on:

- Temperature
- Humidity
- Power consumption
""",
)
def predict_charging_station(data: PredictionInput):

    result = predict_failure(data.temperature, data.humidity, data.power_consumption)

    return {"prediction": result}


@app.post(
    "/operators",
    tags=["Operators"],
    summary="Create an operator",
    response_model=OperatorResponse,
)
def create_operator(operator: OperatorCreate, db: Session = Depends(get_db)):

    new_operator = Operator(
        name=operator.name,
        email=operator.email,
        phone=operator.phone,
        shift=operator.shift,
    )

    db.add(new_operator)
    db.commit()
    db.refresh(new_operator)

    return {"message": "Operator added successfully", "id": new_operator.id}


@app.get(
    "/operators/all",
    tags=["Operators"],
    summary="Get all operators",
    response_model=list[OperatorResponse],
)
def get_all_operators(db: Session = Depends(get_db)):

    operators = db.query(Operator).all()

    return operators


@app.get("/operators", tags=["Operators"], summary="Check operator API")
def get_operators():

    return {"message": "Operator API is working"}


@app.get(
    "/operators/{operator_id}",
    tags=["Operators"],
    summary="Get an operator by ID",
    response_model=OperatorResponse,
)
def get_operator(operator_id: int, db: Session = Depends(get_db)):
    operator = db.query(Operator).filter(Operator.id == operator_id).first()

    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")

    return operator


@app.put(
    "/operators/{operator_id}",
    tags=["Operators"],
    summary="Update an operator",
    response_model=OperatorResponse,
)
def update_operator(
    operator_id: int, operator_data: OperatorUpdate, db: Session = Depends(get_db)
):
    operator = db.query(Operator).filter(Operator.id == operator_id).first()

    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")

    if operator_data.name is not None:
        operator.name = operator_data.name

    if operator_data.email is not None:
        operator.email = operator_data.email

    if operator_data.phone is not None:
        operator.phone = operator_data.phone

    if operator_data.shift is not None:
        operator.shift = operator_data.shift

    db.commit()
    db.refresh(operator)

    return operator


@app.delete(
    "/operators/{operator_id}", tags=["Operators"], summary="Delete an operator"
)
def delete_operator(operator_id: int, db: Session = Depends(get_db)):
    operator = db.query(Operator).filter(Operator.id == operator_id).first()

    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")

    db.delete(operator)
    db.commit()

    return {"message": "Operator deleted successfully"}


@app.post(
    "/prediction",
    tags=["Predictions"],
    summary="Save a prediction",
    response_model=PredictionResponse,
)
def create_prediction(data: PredictionCreate, db: Session = Depends(get_db)):

    prediction = Prediction(
        charging_station_id=data.charging_station_id,
        temperature=data.temperature,
        humidity=data.humidity,
        power_consumption=data.power_consumption,
        prediction=data.prediction,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction


@app.get(
    "/prediction/all",
    tags=["Predictions"],
    summary="Get all predictions",
    response_model=list[PredictionResponse],
)
def get_predictions(db: Session = Depends(get_db)):

    return db.query(Prediction).all()


@app.post(
    "/feedback",
    tags=["Feedback"],
    summary="Create user feedback",
    response_model=FeedbackResponse,
)
def create_feedback(data: FeedbackCreate, db: Session = Depends(get_db)):

    feedback = Feedback(
        user_id=data.user_id,
        charging_station_id=data.charging_station_id,
        comments=data.comments,
        rating=data.rating,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return feedback


@app.get(
    "/prediction/{prediction_id}",
    tags=["Predictions"],
    summary="Get a prediction by ID",
    response_model=PredictionResponse,
)
def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()

    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    return prediction


@app.delete(
    "/prediction/{prediction_id}", tags=["Predictions"], summary="Delete a prediction"
)
def delete_prediction(prediction_id: int, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()

    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    db.delete(prediction)
    db.commit()

    return {"message": "Prediction deleted successfully"}


@app.get(
    "/feedback/all",
    tags=["Feedback"],
    summary="Get all feedback",
    response_model=list[FeedbackResponse],
)
def get_feedback(db: Session = Depends(get_db)):

    return db.query(Feedback).all()


@app.get(
    "/feedback/{feedback_id}",
    tags=["Feedback"],
    summary="Get feedback by ID",
    response_model=FeedbackResponse,
)
def get_feedback_by_id(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()

    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    return feedback


@app.put(
    "/feedback/{feedback_id}",
    tags=["Feedback"],
    summary="Update feedback",
    response_model=FeedbackResponse,
)
def update_feedback(
    feedback_id: int, feedback_data: FeedbackUpdate, db: Session = Depends(get_db)
):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()

    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    if feedback_data.comments is not None:
        feedback.comments = feedback_data.comments

    if feedback_data.rating is not None:
        feedback.rating = feedback_data.rating

    db.commit()
    db.refresh(feedback)

    return feedback


@app.delete("/feedback/{feedback_id}", tags=["Feedback"], summary="Delete feedback")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()

    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    db.delete(feedback)
    db.commit()

    return {"message": "Feedback deleted successfully"}


@app.post(
    "/failure-history",
    tags=["Failure History"],
    summary="Create a failure history record",
    response_model=FailureHistoryResponse,
)
def create_failure_history(data: FailureHistoryCreate, db: Session = Depends(get_db)):

    failure = FailureHistory(
        charging_station_id=data.charging_station_id,
        failure_type=data.failure_type,
        description=data.description,
        failure_date=data.failure_date,
        resolved=data.resolved,
    )

    db.add(failure)
    db.commit()
    db.refresh(failure)

    return failure


@app.get(
    "/failure-history/all",
    tags=["Failure History"],
    summary="Get all failure history records",
    response_model=list[FailureHistoryResponse],
)
def get_all_failure_history(db: Session = Depends(get_db)):

    failures = db.query(FailureHistory).all()

    return failures


@app.get(
    "/failure-history", tags=["Failure History"], summary="Check failure history API"
)
def get_failure_history():
    return {"message": "Failure History API is working"}


@app.get(
    "/failure-history/{failure_id}",
    tags=["Failure History"],
    summary="Get failure history by ID",
    response_model=FailureHistoryResponse,
)
def get_failure_history_by_id(failure_id: int, db: Session = Depends(get_db)):
    failure = db.query(FailureHistory).filter(FailureHistory.id == failure_id).first()

    if not failure:
        raise HTTPException(status_code=404, detail="Failure history record not found")

    return failure


@app.put(
    "/failure-history/{failure_id}",
    tags=["Failure History"],
    summary="Update failure history",
    response_model=FailureHistoryResponse,
)
def update_failure_history(
    failure_id: int, failure_data: FailureHistoryUpdate, db: Session = Depends(get_db)
):
    failure = db.query(FailureHistory).filter(FailureHistory.id == failure_id).first()

    if not failure:
        raise HTTPException(status_code=404, detail="Failure history record not found")

    if failure_data.failure_type is not None:
        failure.failure_type = failure_data.failure_type

    if failure_data.description is not None:
        failure.description = failure_data.description

    if failure_data.failure_date is not None:
        failure.failure_date = failure_data.failure_date

    if failure_data.resolved is not None:
        failure.resolved = failure_data.resolved

    db.commit()
    db.refresh(failure)

    return failure


@app.delete(
    "/failure-history/{failure_id}",
    tags=["Failure History"],
    summary="Delete failure history",
)
def delete_failure_history(failure_id: int, db: Session = Depends(get_db)):
    failure = db.query(FailureHistory).filter(FailureHistory.id == failure_id).first()

    if not failure:
        raise HTTPException(status_code=404, detail="Failure history record not found")

    db.delete(failure)
    db.commit()

    return {"message": "Failure history deleted successfully"}


@app.post(
    "/alerts", tags=["Alerts"], summary="Create an alert", response_model=AlertResponse
)
def create_alert(alert_data: AlertCreate, db: Session = Depends(get_db)):
    new_alert = Alert(
        charging_station_id=alert_data.charging_station_id,
        alert_type=alert_data.alert_type,
        description=alert_data.description,
        is_resolved=alert_data.is_resolved,
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert


@app.get(
    "/alerts/all",
    tags=["Alerts"],
    summary="Get all alerts",
    response_model=list[AlertResponse],
)
def get_all_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).all()
    return alerts


@app.get("/alerts", tags=["Alerts"], summary="Check alerts API", response_model=dict)
def get_alerts():
    return {"message": "Alert API is working"}


@app.get(
    "/alerts/{alert_id}",
    tags=["Alerts"],
    summary="Get an alert by ID",
    response_model=AlertResponse,
)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    return alert


@app.put(
    "/alerts/{alert_id}",
    tags=["Alerts"],
    summary="Update an alert",
    response_model=AlertResponse,
)
def update_alert(alert_id: int, alert_data: AlertUpdate, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    if alert_data.alert_type is not None:
        alert.alert_type = alert_data.alert_type

    if alert_data.description is not None:
        alert.description = alert_data.description

    if alert_data.is_resolved is not None:
        alert.is_resolved = alert_data.is_resolved

    db.commit()
    db.refresh(alert)

    return alert


@app.delete("/alerts/{alert_id}", tags=["Alerts"], summary="Delete an alert")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    db.delete(alert)
    db.commit()

    return {"message": "Alert deleted successfully"}


@app.post(
    "/charging-session",
    tags=["Charging Sessions"],
    summary="Create a charging session",
    response_model=ChargingSessionResponse,
)
def create_charging_session(
    session: ChargingSessionCreate, db: Session = Depends(get_db)
):

    new_session = ChargingSession(
        station_id=session.station_id,
        vehicle_id=session.vehicle_id,
        start_time=session.start_time,
        end_time=session.end_time,
        energy_consumed=session.energy_consumed,
        cost=session.cost,
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session


@app.get(
    "/charging-session/all",
    tags=["Charging Sessions"],
    summary="Get all charging sessions",
    response_model=list[ChargingSessionResponse],
)
def get_all_charging_sessions(db: Session = Depends(get_db)):

    sessions = db.query(ChargingSession).all()

    return sessions


@app.get(
    "/charging-session",
    tags=["Charging Sessions"],
    summary="Check charging session API",
)
def get_charging_session():
    return {"message": "Charging Session API is working"}


@app.get(
    "/charging-session/{session_id}",
    tags=["Charging Sessions"],
    summary="Get a charging session by ID",
    response_model=ChargingSessionResponse,
)
def get_charging_session_by_id(session_id: int, db: Session = Depends(get_db)):
    session = db.query(ChargingSession).filter(ChargingSession.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Charging session not found")

    return session


@app.put(
    "/charging-session/{session_id}",
    tags=["Charging Sessions"],
    summary="Update a charging session",
    response_model=ChargingSessionResponse,
)
def update_charging_session(
    session_id: int, session_data: ChargingSessionUpdate, db: Session = Depends(get_db)
):
    session = db.query(ChargingSession).filter(ChargingSession.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Charging session not found")

    if session_data.vehicle_id is not None:
        session.vehicle_id = session_data.vehicle_id

    if session_data.start_time is not None:
        session.start_time = session_data.start_time

    if session_data.end_time is not None:
        session.end_time = session_data.end_time

    if session_data.energy_consumed is not None:
        session.energy_consumed = session_data.energy_consumed

    if session_data.cost is not None:
        session.cost = session_data.cost

    db.commit()
    db.refresh(session)

    return session


@app.delete(
    "/charging-session/{session_id}",
    tags=["Charging Sessions"],
    summary="Delete a charging session",
)
def delete_charging_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(ChargingSession).filter(ChargingSession.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Charging session not found")

    db.delete(session)
    db.commit()

    return {"message": "Charging session deleted successfully"}


@app.get(
    "/dashboard/summary",
    tags=["System"],
    summary="Get dashboard summary",
    response_model=DashboardSummaryResponse,
)
def get_dashboard_summary(db: Session = Depends(get_db)):

    total_stations = db.query(Machine).count()

    total_telemetry_records = db.query(Telemetry).count()

    total_alerts = db.query(Alert).count()

    unresolved_alerts = db.query(Alert).filter(Alert.is_resolved == False).count()

    total_failures = db.query(FailureHistory).count()

    unresolved_failures = (
        db.query(FailureHistory).filter(FailureHistory.resolved == "No").count()
    )

    total_maintenance = db.query(Maintenance).count()

    pending_maintenance = (
        db.query(Maintenance).filter(Maintenance.status == "Pending").count()
    )

    total_charging_sessions = db.query(ChargingSession).count()

    total_operators = db.query(Operator).count()

    total_predictions = db.query(Prediction).count()

    return {
        "total_stations": total_stations,
        "total_telemetry_records": total_telemetry_records,
        "total_alerts": total_alerts,
        "unresolved_alerts": unresolved_alerts,
        "total_failures": total_failures,
        "unresolved_failures": unresolved_failures,
        "total_maintenance": total_maintenance,
        "pending_maintenance": pending_maintenance,
        "total_charging_sessions": total_charging_sessions,
        "total_operators": total_operators,
        "total_predictions": total_predictions,
    }
