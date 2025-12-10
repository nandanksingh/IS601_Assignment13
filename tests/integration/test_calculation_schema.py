# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-12: Calculation Schema Tests
# File: tests/integration/test_calculation_schema.py
# ----------------------------------------------------------
# Description:
# Tests Pydantic schemas responsible for validating calculation
# input and producing structured outputs. Ensures that supported
# operation types compute results correctly, invalid operation
# types raise errors, divide-by-zero is rejected, and response
# schemas return well-structured data objects.
# ----------------------------------------------------------

import pytest
from pydantic import ValidationError
from app.schemas.cal_schemas import CalculationCreate, CalculationRead


# ----------------------------------------------------------
# Valid calculation creation should auto-compute result
# ----------------------------------------------------------
def test_create_schema_valid():
    schema = CalculationCreate(type="add", a=3, b=5)

    # Automatic computation handled by model validator
    assert schema.result == 8
    assert schema.type == "add"
    assert schema.a == 3
    assert schema.b == 5


# ----------------------------------------------------------
# Unsupported operation types must raise validation error
# ----------------------------------------------------------
def test_invalid_type():
    with pytest.raises(ValidationError):
        CalculationCreate(type="power", a=2, b=3)


# ----------------------------------------------------------
# Division by zero validation
# ----------------------------------------------------------
def test_divide_by_zero_invalid():
    with pytest.raises(ValidationError):
        CalculationCreate(type="divide", a=10, b=0)


# ----------------------------------------------------------
# Read schema validation and field assignment
# ----------------------------------------------------------
def test_read_schema_values():
    read = CalculationRead(
        id=1,
        type="add",
        a=1,
        b=1,
        result=2,
        user_id=5,
    )

    assert read.id == 1
    assert read.result == 2
    assert read.type == "add"
    assert read.user_id == 5
