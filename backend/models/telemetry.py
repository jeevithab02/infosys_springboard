# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, Float, ForeignKey

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship

# pyrefly: ignore [missing-import]
from backend.database.connection import Base


class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)

    charging_station_id = Column(
        Integer, ForeignKey("charging_stations.id"), nullable=False, index=True
    )

    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    power_consumption = Column(Float, nullable=False)

    station = relationship("Machine", back_populates="telemetry")
