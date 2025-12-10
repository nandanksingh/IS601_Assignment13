# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Calculation Model
# File: app/models/cal_models.py
# ----------------------------------------------------------
# Description:
# SQLAlchemy ORM model representing a user-owned calculation.
# Includes:
#   • Operation type (add/subtract/multiply/divide)
#   • Input numbers a and b
#   • Result value (nullable for error cases)
#   • created_at timestamp (fixes N/A date issue in dashboard)
#   • Foreign key to User model
# ----------------------------------------------------------

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship
from app.database.dbase import Base


class Calculation(Base):
    __tablename__ = "calculations"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Operation fields
    type = Column(String, nullable=False)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)

    # Result may be null (example: divide-by-zero)
    result = Column(Float, nullable=True)

    # NEW FIELD — fixes "N/A" in dashboard history
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Foreign key reference to User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship back to User.calculations
    user = relationship("User", back_populates="calculations")
