# pyrefly: ignore [missing-import]
from pydantic import BaseModel


class StationHealthResponse(BaseModel):
    station_id: int
    station_name: str

    temperature: float | None = None
    humidity: float | None = None
    power_consumption: float | None = None

    active_alerts: int
    recent_failures: int
    maintenance_status: str | None = None

    health: str
