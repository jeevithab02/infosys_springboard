# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict, Field


class PredictionCreate(BaseModel):
    charging_station_id: int

    temperature: float
    humidity: float = Field(..., ge=0, le=100)

    power_consumption: float = Field(..., ge=0)

    prediction: str


class PredictionResponse(BaseModel):
    id: int
    charging_station_id: int
    temperature: float
    humidity: float
    power_consumption: float
    prediction: str

    model_config = ConfigDict(from_attributes=True)
