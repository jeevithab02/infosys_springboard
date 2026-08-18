# pyrefly: ignore [missing-import]
from pydantic import BaseModel


class StationAnalyticsResponse(BaseModel):
    station_id: int
    station_name: str

    average_temperature: float | None = None
    average_humidity: float | None = None
    average_power_consumption: float | None = None

    total_energy_consumed: float
    total_charging_cost: float
    total_charging_sessions: int

    total_alerts: int
    unresolved_alerts: int

    total_failures: int
    unresolved_failures: int

    total_maintenance: int
