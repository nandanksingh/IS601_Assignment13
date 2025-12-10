# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-12 / 13: Calculation Schemas
# File: app/schemas/cal_schemas.py
# ----------------------------------------------------------
# Description:
# Pydantic schemas for calculation creation, reading, and
# database serialization. Includes validation for operation
# type, divide-by-zero protection, and automatic result
# computation using Pydantic v2 model validators.
# ----------------------------------------------------------

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator, ValidationInfo

# Allowed operation types
ALLOWED_TYPES = {"add", "subtract", "multiply", "divide"}


# ----------------------------------------------------------
# Calculation Create Schema
# ----------------------------------------------------------
class CalculationCreate(BaseModel):
    type: str
    a: float
    b: float
    result: Optional[float] = None

    # Validate operation name
    @field_validator("type")
    def validate_type(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ALLOWED_TYPES:
            raise ValueError("Unsupported calculation type")
        return v

    # Prevent division by zero
    @field_validator("b")
    def validate_division(cls, b: float, info: ValidationInfo):
        if info.data.get("type") == "divide" and b == 0:
            raise ValueError("Division by zero")
        return b

    # Auto-compute result after validation
    @model_validator(mode="after")
    def compute_result(self):
        if self.type == "add":
            self.result = self.a + self.b
        elif self.type == "subtract":
            self.result = self.a - self.b
        elif self.type == "multiply":
            self.result = self.a * self.b
        elif self.type == "divide":
            self.result = self.a / self.b
        return self


# ----------------------------------------------------------
# Calculation Read Schema (API response)
# ----------------------------------------------------------
class CalculationRead(BaseModel):
    id: int
    type: str
    a: float
    b: float
    result: float
    user_id: int
    created_at: Optional[datetime] = None   

    model_config = {"from_attributes": True}


class CalculationDBRead(CalculationRead):
    pass
