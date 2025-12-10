# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-12 / 13: Calculation CRUD Routes
# File: app/routers/calc.py
# ----------------------------------------------------------
# Description:
# CRUD routes for arithmetic calculations.
# Each calculation belongs to the authenticated user.
# Includes correct created_at support for Assignment-13 UI.
# ----------------------------------------------------------

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.cal_models import Calculation
from app.schemas.cal_schemas import CalculationCreate, CalculationRead
from app.database.dbase import get_db
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/calculations", tags=["Calculations"])


# ----------------------------------------------------------
# Helper: Calculator Engine
# ----------------------------------------------------------
def compute_result(calc_type: str, a: float, b: float) -> float:
    calc_type = calc_type.strip().lower()

    if calc_type == "add":
        return a + b
    if calc_type == "subtract":
        return a - b
    if calc_type == "multiply":
        return a * b
    if calc_type == "divide":
        if b == 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Division by zero"
            )
        return a / b

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Invalid operation type"
    )


# ----------------------------------------------------------
# CREATE
# ----------------------------------------------------------
@router.post("", response_model=CalculationRead, status_code=status.HTTP_201_CREATED)
def create_calculation(
    payload: CalculationCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new calculation for the authenticated user."""

    result = compute_result(payload.type, payload.a, payload.b)

    calc = Calculation(
        type=payload.type,
        a=payload.a,
        b=payload.b,
        result=result,
        user_id=user.id,
    )

    db.add(calc)
    db.commit()
    db.refresh(calc)  # loads created_at

    return calc


# ----------------------------------------------------------
# LIST (History)
# ----------------------------------------------------------
@router.get("", response_model=list[CalculationRead])
def list_calculations(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return all user calculations sorted by newest first."""
    return (
        db.query(Calculation)
        .filter(Calculation.user_id == user.id)
        .order_by(Calculation.created_at.desc())
        .all()
    )


# ----------------------------------------------------------
# READ
# ----------------------------------------------------------
@router.get("/{calc_id}", response_model=CalculationRead)
def read_calculation(
    calc_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    calc = (
        db.query(Calculation)
        .filter(Calculation.id == calc_id, Calculation.user_id == user.id)
        .first()
    )

    if not calc:
        raise HTTPException(404, detail="Calculation not found")

    return calc


# ----------------------------------------------------------
# UPDATE
# ----------------------------------------------------------
@router.put("/{calc_id}", response_model=CalculationRead)
def update_calculation(
    calc_id: int,
    payload: CalculationCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    calc = (
        db.query(Calculation)
        .filter(Calculation.id == calc_id, Calculation.user_id == user.id)
        .first()
    )

    if not calc:
        raise HTTPException(404, detail="Calculation not found")

    calc.type = payload.type
    calc.a = payload.a
    calc.b = payload.b
    calc.result = compute_result(payload.type, payload.a, payload.b)

    db.commit()
    db.refresh(calc)

    return calc


# ----------------------------------------------------------
# DELETE
# ----------------------------------------------------------
@router.delete("/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(
    calc_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    calc = (
        db.query(Calculation)
        .filter(Calculation.id == calc_id, Calculation.user_id == user.id)
        .first()
    )

    if not calc:
        raise HTTPException(404, detail="Calculation not found")

    db.delete(calc)
    db.commit()
    return None
