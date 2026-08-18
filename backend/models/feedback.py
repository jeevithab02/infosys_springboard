# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, ForeignKey

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship

from backend.database.connection import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    charging_station_id = Column(
        Integer, ForeignKey("charging_stations.id"), nullable=False
    )

    comments = Column(String)
    rating = Column(Integer, nullable=False)

    user = relationship("User", back_populates="feedback")

    station = relationship("Machine", back_populates="feedback")
