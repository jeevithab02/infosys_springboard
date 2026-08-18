from datetime import datetime

# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict


class AlertCreate(BaseModel):
    charging_station_id: int
    alert_type: str
    description: str
    is_resolved: bool = False


class AlertUpdate(BaseModel):
    alert_type: str | None = None
    description: str | None = None
    is_resolved: bool | None = None


class AlertResponse(BaseModel):
    id: int
    charging_station_id: int
    alert_type: str
    description: str
    is_resolved: bool
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
