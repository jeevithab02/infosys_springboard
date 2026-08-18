# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, Float, String, ForeignKey

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship

# pyrefly: ignore [missing-import]
from backend.database.connection import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    charging_station_id = Column(
        Integer, ForeignKey("charging_stations.id"), nullable=False, index=True
    )

    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    power_consumption = Column(Float, nullable=False)

    prediction = Column(String, nullable=False)

    station = relationship("Machine", back_populates="predictions")
