from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.alert import Alert
from backend.schemas.alert import AlertCreate, AlertResponse


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)

@router.post("/", response_model=dict)
def create_alert(alert_data: AlertCreate, db: Session = Depends(get_db)):

    new_alert = Alert(
        charging_station_id=alert_data.charging_station_id,
        alert_type=alert_data.alert_type,
        description=alert_data.description,
        is_resolved=alert_data.is_resolved
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return {
        "message": "Alert added successfully",
        "id": new_alert.id
    }

@router.get("/all", response_model=list[AlertResponse])
def get_all_alerts(db: Session = Depends(get_db)):

    alerts = db.query(Alert).all()

    return alerts

@router.get("/", response_model=dict)
def get_alerts():
    return {
        "message": "Alert API is working"
    }
