# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict


class MachineCreate(BaseModel):
    station_name: str
    charger_type: str
    location: str


class MachineUpdate(BaseModel):
    station_name: str | None = None
    charger_type: str | None = None
    location: str | None = None


class MachineResponse(BaseModel):
    id: int
    station_name: str
    charger_type: str
    location: str

    model_config = ConfigDict(from_attributes=True)
