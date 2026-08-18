from datetime import datetime

# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict


class MaintenanceCreate(BaseModel):
    charging_station_id: int
    maintenance_date: datetime
    status: str


class MaintenanceUpdate(BaseModel):
    maintenance_date: datetime | None = None
    status: str | None = None


class MaintenanceResponse(BaseModel):
    id: int
    charging_station_id: int
    maintenance_date: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)
