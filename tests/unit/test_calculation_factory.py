# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-12: Calculation Factory Tests
# File: tests/unit/test_calculation_factory.py
# ----------------------------------------------------------
# Description:
# Unit tests for the CalculationFactory and its operation
# strategies. Verifies correct operation creation, expected
# compute() results, rejection of unsupported operation types,
# and proper handling of divide-by-zero cases. Ensures the
# factory returns working operation instances.
# ----------------------------------------------------------

import pytest
from app.factory.calculation_factory import CalculationFactory


# ----------------------------------------------------------
# Factory behavior tests for supported operations
# ----------------------------------------------------------
@pytest.mark.parametrize(
    "calc_type, expected_result",
    [
        ("add", 12),
        ("subtract", 8),
        ("sub", 8),
        ("minus", 8),
        ("multiply", 20),
        ("mul", 20),
        ("divide", 5),
        ("div", 5),
    ],
)
def test_factory_returns_correct_operation(calc_type, expected_result):
    op = CalculationFactory.create(calc_type)

    # Factory must return an object that has compute()
    assert hasattr(op, "compute")

    # Verify compute() produces correct result
    assert op.compute(10, 2) == expected_result


# ----------------------------------------------------------
# Unsupported operation names must raise errors
# ----------------------------------------------------------
@pytest.mark.parametrize("invalid_type", ["", "   ", "xyz", "unknown", "power"])
def test_factory_invalid_type_raises(invalid_type):
    with pytest.raises(ValueError, match="Unsupported calculation type"):
        CalculationFactory.create(invalid_type)


# ----------------------------------------------------------
# Individual operation behavior tests
# ----------------------------------------------------------
def test_add_operation_compute():
    op = CalculationFactory.create("add")
    assert op.compute(5, 7) == 12


def test_subtract_operation_compute():
    op = CalculationFactory.create("subtract")
    assert op.compute(10, 4) == 6


def test_multiply_operation_compute():
    op = CalculationFactory.create("multiply")
    assert op.compute(3, 5) == 15


def test_divide_operation_compute():
    op = CalculationFactory.create("divide")
    assert op.compute(20, 5) == 4


def test_divide_operation_zero_error():
    op = CalculationFactory.create("divide")
    with pytest.raises(ValueError, match="Division by zero"):
        op.compute(10, 0)
