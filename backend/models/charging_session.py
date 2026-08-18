# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship

# pyrefly: ignore [missing-import]
from backend.database.connection import Base


class ChargingSession(Base):
    __tablename__ = "charging_sessions"

    id = Column(Integer, primary_key=True, index=True)

    station_id = Column(
        Integer, ForeignKey("charging_stations.id"), nullable=False, index=True
    )

    vehicle_id = Column(String, nullable=False)

    start_time = Column(DateTime)
    end_time = Column(DateTime)

    energy_consumed = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)

    station = relationship("Machine", back_populates="charging_sessions")
