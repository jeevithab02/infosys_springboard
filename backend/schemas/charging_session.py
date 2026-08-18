from datetime import datetime

# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict, Field


class ChargingSessionCreate(BaseModel):
    station_id: int
    vehicle_id: str
    start_time: datetime
    end_time: datetime
    energy_consumed: float = Field(..., ge=0)
    cost: float = Field(..., ge=0)


class ChargingSessionUpdate(BaseModel):
    vehicle_id: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    energy_consumed: float | None = Field(default=None, ge=0)
    cost: float | None = Field(default=None, ge=0)


class ChargingSessionResponse(BaseModel):
    id: int
    station_id: int
    vehicle_id: str
    start_time: datetime
    end_time: datetime
    energy_consumed: float
    cost: float

    model_config = ConfigDict(from_attributes=True)
