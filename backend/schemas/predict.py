# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    charging_station_id: int

    temperature: float

    humidity: float = Field(..., ge=0, le=100)

    power_consumption: float = Field(..., ge=0)
