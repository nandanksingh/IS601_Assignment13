# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: User SQLAlchemy Model
# File: app/models/user_model.py
# ----------------------------------------------------------
# Description:
# SQLAlchemy ORM user model providing:
#   • Core identity fields (first/last name, username, email)
#   • Optional mobile number (no unique constraint)
#   • Password hashing and verification helpers
#   • Automatic timestamps
#   • Relationship to Calculation model
# Fully aligned with Assignment-13 + integration test behavior.
# ----------------------------------------------------------

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.database.dbase import Base
from app.schemas.user_schema import UserResponse
from app.auth.security import hash_password, verify_password


class User(Base):
    __tablename__ = "users"

    # ------------------------------------------------------
    # Core Identity Fields
    # ------------------------------------------------------
    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)

    # ------------------------------------------------------
    # Mobile number is OPTIONAL and NOT UNIQUE
    # Tests create many users without mobile, so uniqueness
    # must not be enforced.
    # ------------------------------------------------------
    mobile = Column(String(15), nullable=True, index=True, default=None)

    is_active = Column(Boolean, nullable=False, default=True)

    # ------------------------------------------------------
    # Authentication
    # ------------------------------------------------------
    password_hash = Column(String(255), nullable=False)

    # ------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )

    # ------------------------------------------------------
    # Unique Constraints — username + email only
    # Mobile constraint removed (required by tests)
    # ------------------------------------------------------
    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
        UniqueConstraint("email", name="uq_users_email"),
    )

    # ------------------------------------------------------
    # Relationship: One User → Many Calculations
    # ------------------------------------------------------
    calculations = relationship(
        "Calculation",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # ------------------------------------------------------
    # Password Utilities
    # ------------------------------------------------------
    def set_password(self, raw_password: str):
        if not raw_password:
            raise ValueError("Password cannot be empty")
        self.password_hash = hash_password(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        try:
            return verify_password(raw_password, self.password_hash)
        except Exception:
            return False

    # ------------------------------------------------------
    # ORM → Pydantic Schema Conversion
    # ------------------------------------------------------
    def to_read_schema(self) -> UserResponse:
        return UserResponse.model_validate({
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "mobile": self.mobile,
            "is_active": self.is_active,
        })

    # ------------------------------------------------------
    # Debug Output
    # ------------------------------------------------------
    def __repr__(self):
        return (
            f"User(id={self.id}, username='{self.username}', "
            f"email='{self.email}', mobile='{self.mobile}')"
        )
