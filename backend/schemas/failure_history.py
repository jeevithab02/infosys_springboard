from datetime import datetime

# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict


class FailureHistoryCreate(BaseModel):
    charging_station_id: int
    failure_type: str
    description: str | None = None
    failure_date: datetime
    resolved: str = "No"


class FailureHistoryUpdate(BaseModel):
    failure_type: str | None = None
    description: str | None = None
    failure_date: datetime | None = None
    resolved: str | None = None


class FailureHistoryResponse(BaseModel):
    id: int
    charging_station_id: int
    failure_type: str
    description: str | None
    failure_date: datetime
    resolved: str

    model_config = ConfigDict(from_attributes=True)
