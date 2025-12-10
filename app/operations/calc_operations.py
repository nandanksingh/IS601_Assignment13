# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-12: Arithmetic Operations Module
# File: app/operations/calc_operations.py
# ----------------------------------------------------------
# Description:
# Defines core arithmetic operations used throughout the
# calculator system. Provides both pure function-based
# operations and class-based operation objects, ensuring
# strict numeric validation and predictable behavior. These
# utilities support the factory pattern and unit testing
# requirements across the project.
# ----------------------------------------------------------

from typing import Union

# Numeric types allowed for all operations
Number = Union[int, float]


# ----------------------------------------------------------
# Shared numeric validator for all arithmetic operations
# Ensures input values are numeric and converts them to float
# ----------------------------------------------------------
def _validate(value: Number) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError("Input must be numeric.")
    return float(value)


# ----------------------------------------------------------
# Function-based operations
# These are directly used in unit tests and must preserve
# exact error messages and numeric validation behavior
# ----------------------------------------------------------
def add(a: Number, b: Number) -> float:
    a, b = _validate(a), _validate(b)
    return a + b


def subtract(a: Number, b: Number) -> float:
    a, b = _validate(a), _validate(b)
    return a - b


def multiply(a: Number, b: Number) -> float:
    a, b = _validate(a), _validate(b)
    return a * b


def divide(a: Number, b: Number) -> float:
    a, b = _validate(a), _validate(b)
    if b == 0:
        raise ValueError("Division by zero")
    return a / b


# ----------------------------------------------------------
# Class-based operations
# These are used by CalculationFactory to construct objects
# that encapsulate specific arithmetic behaviors
# ----------------------------------------------------------
class AddOperation:
    """Perform addition using a stored pair of operands."""

    def __init__(self, a: Number, b: Number):
        self.a = a
        self.b = b

    def compute(self) -> float:
        return add(self.a, self.b)


class SubtractOperation:
    """Perform subtraction using stored operands."""

    def __init__(self, a: Number, b: Number):
        self.a = a
        self.b = b

    def compute(self) -> float:
        return subtract(self.a, self.b)


class MultiplyOperation:
    """Perform multiplication using stored operands."""

    def __init__(self, a: Number, b: Number):
        self.a = a
        self.b = b

    def compute(self) -> float:
        return multiply(self.a, self.b)


class DivideOperation:
    """Perform safe division with validation."""

    def __init__(self, a: Number, b: Number):
        self.a = a
        self.b = b

    def compute(self) -> float:
        return divide(self.a, self.b)


# Allow clean wildcard imports in other modules
__all__ = [
    "add",
    "subtract",
    "multiply",
    "divide",
    "AddOperation",
    "SubtractOperation",
    "MultiplyOperation",
    "DivideOperation",
]
