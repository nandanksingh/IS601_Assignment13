# ----------------------------------------------------------
# Author: Nandan Kumar
# Date: 11/17/2025
# Assignment-11/12: Calculation Logic Unit Tests
# File: tests/unit/test_calculator.py
# ----------------------------------------------------------
# Description:
# Unit tests for the arithmetic utility functions defined in
# app/operations/__init__.py (add, subtract, multiply, divide).
# Ensures correctness of results, numeric type validation,
# float-normalized outputs, and proper division-by-zero errors.
# Provides full coverage for calculator helper functions.
# ----------------------------------------------------------

import pytest
from app.operations import add, subtract, multiply, divide


# ----------------------------------------------------------
# add()
# ----------------------------------------------------------
@pytest.mark.parametrize("a, b, expected", [
    (3, 5, 8),
    (-2, 6, 4),
    (2.5, 1.5, 4.0),
    (0, 0, 0),
])
def test_add(a, b, expected):
    """Verify add() produces correct sums across numeric types."""
    assert add(a, b) == expected


# ----------------------------------------------------------
# subtract()
# ----------------------------------------------------------
@pytest.mark.parametrize("a, b, expected", [
    (10, 4, 6),
    (4, 10, -6),
    (-3, -2, -1),
    (7.5, 2.5, 5.0),
])
def test_subtract(a, b, expected):
    """Verify subtract() handles positive, negative, and float values."""
    assert subtract(a, b) == expected


# ----------------------------------------------------------
# multiply()
# ----------------------------------------------------------
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 6),
    (-2, 3, -6),
    (1.5, 2.0, 3.0),
    (0, 7, 0),
])
def test_multiply(a, b, expected):
    """Ensure multiply() produces correct products."""
    assert multiply(a, b) == expected


# ----------------------------------------------------------
# divide()
# ----------------------------------------------------------
@pytest.mark.parametrize("a, b, expected", [
    (8, 2, 4.0),
    (-9, 3, -3.0),
    (7.5, 2.5, 3.0),
    (0, 5, 0.0),
])
def test_divide(a, b, expected):
    """Verify divide() returns correct float results."""
    assert divide(a, b) == expected


# ----------------------------------------------------------
# divide → ZeroDivision
# ----------------------------------------------------------
def test_divide_by_zero():
    """Division by zero should raise ValueError."""
    with pytest.raises(ValueError, match="Division by zero"):
        divide(10, 0)


# ----------------------------------------------------------
# Invalid Types
# ----------------------------------------------------------
@pytest.mark.parametrize("func, a, b", [
    (add, "abc", 5),
    (subtract, 3, None),
    (multiply, [1, 2], 4),
    (divide, 5, "xyz"),
])
def test_invalid_type_inputs(func, a, b):
    """Invalid numeric inputs must raise ValueError (validate_number())."""
    with pytest.raises(ValueError, match="Input must be numeric"):
        func(a, b)
