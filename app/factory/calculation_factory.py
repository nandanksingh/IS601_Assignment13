# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Calculation Factory
# File: app/factory/calculation_factory.py
# ----------------------------------------------------------
# Description:
# Central factory for creating arithmetic operation objects.
# Normalizes operation names, supports synonyms, and returns
# an instance of the correct operation class.
# ----------------------------------------------------------


# ----------------------------------------------------------
# Arithmetic Operation Classes
# ----------------------------------------------------------
class AddOperation:
    @staticmethod
    def compute(a: float, b: float) -> float:
        return a + b


class SubtractOperation:
    @staticmethod
    def compute(a: float, b: float) -> float:
        return a - b


class MultiplyOperation:
    @staticmethod
    def compute(a: float, b: float) -> float:
        return a * b


class DivideOperation:
    @staticmethod
    def compute(a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero")
        return a / b


# ----------------------------------------------------------
# Calculation Factory
# ----------------------------------------------------------
class CalculationFactory:
    """
    Maps normalized operation names to concrete operation classes.
    Returns instantiated operation objects.
    """

    OPERATIONS = {
        # Addition
        "add": AddOperation,
        "addition": AddOperation,
        "plus": AddOperation,

        # Subtraction
        "subtract": SubtractOperation,
        "sub": SubtractOperation,
        "minus": SubtractOperation,

        # Multiplication
        "multiply": MultiplyOperation,
        "mul": MultiplyOperation,
        "times": MultiplyOperation,

        # Division
        "divide": DivideOperation,
        "div": DivideOperation,
        "division": DivideOperation,
    }

    @classmethod
    def create(cls, op_type: str):
        """
        Normalize the operation string and return an instance of the
        associated operation class.
        """
        key = op_type.strip().lower()

        if key not in cls.OPERATIONS:
            raise ValueError("Unsupported calculation type")

        operation_class = cls.OPERATIONS[key]
        return operation_class()
