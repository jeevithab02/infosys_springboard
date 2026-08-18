# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship

from backend.database.connection import Base


class Machine(Base):
    __tablename__ = "charging_stations"

    id = Column(Integer, primary_key=True, index=True)
    station_name = Column(String, nullable=False)
    charger_type = Column(String, nullable=False)
    location = Column(String, nullable=False)

    telemetry = relationship(
        "Telemetry", back_populates="station", cascade="all, delete-orphan"
    )

    maintenance_records = relationship(
        "Maintenance", back_populates="station", cascade="all, delete-orphan"
    )

    alerts = relationship(
        "Alert", back_populates="station", cascade="all, delete-orphan"
    )

    charging_sessions = relationship(
        "ChargingSession", back_populates="station", cascade="all, delete-orphan"
    )

    failure_history = relationship(
        "FailureHistory", back_populates="station", cascade="all, delete-orphan"
    )

    predictions = relationship(
        "Prediction", back_populates="station", cascade="all, delete-orphan"
    )

    feedback = relationship(
        "Feedback", back_populates="station", cascade="all, delete-orphan"
    )
