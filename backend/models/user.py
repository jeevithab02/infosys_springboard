# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship

# pyrefly: ignore [missing-import]
from backend.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    feedback = relationship(
        "Feedback", back_populates="user", cascade="all, delete-orphan"
    )
