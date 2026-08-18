# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship

# pyrefly: ignore [missing-import]
from backend.database.connection import Base


class Maintenance(Base):
    __tablename__ = "maintenance"

    id = Column(Integer, primary_key=True, index=True)

    charging_station_id = Column(
        Integer, ForeignKey("charging_stations.id"), nullable=False, index=True
    )

    maintenance_date = Column(DateTime, nullable=False)

    status = Column(String, nullable=False)

    station = relationship("Machine", back_populates="maintenance_records")
