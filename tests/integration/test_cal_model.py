# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-12: Calculation Model Tests
# File: tests/integration/test_cal_model.py
# ----------------------------------------------------------
# Description:
# Tests SQLAlchemy Calculation model behavior including inserts,
# arithmetic value storage, querying, and user-link association.
# Ensures calculation rows persist correctly, parameters are stored
# accurately, and the model handles basic persistence without relying
# on API-level validation rules.
# ----------------------------------------------------------

import pytest
from app.models.cal_models import Calculation


# ----------------------------------------------------------
# Insert and basic field verification
# ----------------------------------------------------------
def test_insert_calculation(db_session, test_user):
    calc = Calculation(
        type="add",
        a=10,
        b=5,
        result=15,
        user_id=test_user.id,
    )

    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)

    # Verify the row stored the correct data
    assert calc.result == 15
    assert calc.type == "add"
    assert calc.user_id == test_user.id


# ----------------------------------------------------------
# Test multiple operation types
# ----------------------------------------------------------
@pytest.mark.parametrize(
    "op_type, a, b, expected",
    [
        ("add", 1, 2, 3),
        ("subtract", 10, 3, 7),
        ("multiply", 2, 3, 6),
        ("divide", 20, 5, 4),
    ],
)
def test_all_operations(db_session, test_user, op_type, a, b, expected):
    calc = Calculation(
        type=op_type,
        a=a,
        b=b,
        result=expected,
        user_id=test_user.id,
    )

    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)

    # Model stores whatever values are given
    assert calc.result == expected
    assert calc.type == op_type


# ----------------------------------------------------------
# Foreign key behavior (SQLite does not enforce by default)
# ----------------------------------------------------------
def test_invalid_user_id_allowed(db_session):
    calc = Calculation(
        type="add",
        a=5,
        b=5,
        result=10,
        user_id=999999,        # intentionally invalid FK
    )

    db_session.add(calc)
    db_session.commit()

    # Record still persists because FK constraints are not enforced in SQLite tests
    stored = db_session.query(Calculation).filter_by(user_id=999999).first()
    assert stored is not None


# ----------------------------------------------------------
# Division-by-zero is NOT validated at the model layer
# ----------------------------------------------------------
def test_model_allows_division_by_zero(db_session, test_user):
    calc = Calculation(
        type="divide",
        a=10,
        b=0,                   # model-level should allow
        result=None,
        user_id=test_user.id,
    )

    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)

    # Model accepts the row; API layer handles validation separately
    assert calc.b == 0
    assert calc.result is None
