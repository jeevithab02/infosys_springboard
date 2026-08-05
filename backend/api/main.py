from fastapi import FastAPI
from backend.database.connection import engine, Base
from backend.models.user import User
from backend.models.machine import Machine
from backend.schemas.machine import MachineCreate
from backend.models.telemetry import Telemetry
# pyrefly: ignore [missing-import]
from backend.schemas.telemetry import TelemetryCreate
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.models.maintenance import Maintenance
# pyrefly: ignore [missing-import]
from backend.schemas.maintenance import MaintenanceCreate   

from backend.database.connection import get_db
from backend.schemas.user import UserCreate
from backend.ml.predict import predict_failure
from backend.schemas.predict import PredictionInput
from backend.models.prediction import Prediction
# pyrefly: ignore [missing-import]
from backend.schemas.prediction import PredictionCreate

from backend.models.feedback import Feedback
# pyrefly: ignore [missing-import]
from backend.schemas.feedback import FeedbackCreate 

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EV Charging Station Health Monitoring API",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "EV Charging Station Health Monitoring Backend Running"
    }

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User added successfully",
        "id": new_user.id
    }

@app.get("/users/all")
def get_all_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return users

@app.get("/users")
def get_users():
    return {
        "message": "User API is working"
    }

@app.post("/charging-stations")
def create_charging_station(machine_data: MachineCreate, db: Session = Depends(get_db)):

    charging_station = Machine(
        station_name=machine_data.station_name,
        charger_type=machine_data.charger_type,
        location=machine_data.location
    )

    db.add(charging_station)
    db.commit()
    db.refresh(charging_station)

    return {
        "message": "Charging station added successfully",
        "id": charging_station.id
    }


@app.get("/charging-stations/all")
def get_all_charging_stations(db: Session = Depends(get_db)):

    charging_stations = db.query(Machine).all()

    return charging_stations


@app.get("/charging-stations")
def get_charging_stations():
    return {
        "message": "Charging station API is working"
    }

@app.post("/telemetry")
def create_telemetry(telemetry_data: TelemetryCreate, db: Session = Depends(get_db)):

    telemetry = Telemetry(
        charging_station_id=telemetry_data.charging_station_id,
        temperature=telemetry_data.temperature,
        humidity=telemetry_data.humidity,
        power_consumption=telemetry_data.power_consumption
    )

    db.add(telemetry)
    db.commit()
    db.refresh(telemetry)

    return {
        "message": "Telemetry added successfully",
        "id": telemetry.id
    }


@app.get("/telemetry/all")
def get_all_telemetry(db: Session = Depends(get_db)):

    telemetry = db.query(Telemetry).all()

    return telemetry


@app.get("/telemetry")
def get_telemetry():
    return {
        "message": "Telemetry API is working"
    }

@app.post("/maintenance")
def create_maintenance(data: MaintenanceCreate, db: Session = Depends(get_db)):

    maintenance = Maintenance(
        charging_station_id=data.charging_station_id,
        maintenance_date=data.maintenance_date,
        status=data.status
    )

    db.add(maintenance)
    db.commit()
    db.refresh(maintenance)

    return {
        "message": "Maintenance record added successfully",
        "id": maintenance.id
    }

@app.get("/maintenance/all")
def get_all_maintenance(db: Session = Depends(get_db)):

    maintenance = db.query(Maintenance).all()

    return maintenance

@app.post("/predict")
def predict_charging_station(data: PredictionInput):

    result = predict_failure(
        data.temperature,
        data.humidity,
        data.power_consumption
    )

    return {
        "prediction": result
    }

@app.post("/prediction")
def create_prediction(data: PredictionCreate, db: Session = Depends(get_db)):

    prediction = Prediction(
        temperature=data.temperature,
        humidity=data.humidity,
        power_consumption=data.power_consumption,
        prediction=data.prediction
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return {
        "message": "Prediction saved successfully",
        "id": prediction.id
    }


@app.get("/prediction/all")
def get_predictions(db: Session = Depends(get_db)):
    return db.query(Prediction).all()

@app.post("/feedback")
def create_feedback(data: FeedbackCreate, db: Session = Depends(get_db)):

    feedback = Feedback(
        user_name=data.user_name,
        comments=data.comments,
        rating=data.rating
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return {
        "message": "Feedback added successfully",
        "id": feedback.id
    }


@app.get("/feedback/all")
def get_feedback(db: Session = Depends(get_db)):
    return db.query(Feedback).all()    

