# pyrefly: ignore [missing-import]
from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_stations: int
    total_telemetry_records: int
    total_alerts: int
    unresolved_alerts: int
    total_failures: int
    unresolved_failures: int
    total_maintenance: int
    pending_maintenance: int
    total_charging_sessions: int
    total_operators: int
    total_predictions: int
