# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship

import datetime

# pyrefly: ignore [missing-import]
from backend.database.connection import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    charging_station_id = Column(
        Integer, ForeignKey("charging_stations.id"), nullable=False, index=True
    )

    alert_type = Column(String, index=True)
    description = Column(String)
    is_resolved = Column(Boolean, default=False)

    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    station = relationship("Machine", back_populates="alerts")
