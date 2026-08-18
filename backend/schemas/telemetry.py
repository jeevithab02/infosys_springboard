# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict, Field


class TelemetryCreate(BaseModel):
    charging_station_id: int

    temperature: float = Field(..., description="Charging station temperature in °C")

    humidity: float = Field(..., ge=0, le=100, description="Humidity percentage")

    power_consumption: float = Field(..., ge=0, description="Power consumption in kW")


class TelemetryUpdate(BaseModel):
    temperature: float | None = None
    humidity: float | None = Field(default=None, ge=0, le=100)
    power_consumption: float | None = Field(default=None, ge=0)


class TelemetryResponse(BaseModel):
    id: int
    charging_station_id: int
    temperature: float
    humidity: float
    power_consumption: float

    model_config = ConfigDict(from_attributes=True)
