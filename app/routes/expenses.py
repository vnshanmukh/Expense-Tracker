from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate, ExpenseFilter
from app.services.expenses import (
    create_expense, 
    get_expenses, 
    get_expense_by_id, 
    update_expense, 
    delete_expense
)
from app.security.jwt import get_current_user
from app.models.user import User
from app.models.expense import PaymentMode
from app.utils.rate_limiter import limiter

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("2/minute")
def create_new_expense(
    request:Request,
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new expense
    """
    return create_expense(db=db, expense_data=expense_data, user_id=current_user.id)


@router.get("/", response_model=List[ExpenseResponse])
def read_expenses(
    category: Optional[str] = None,
    payment_mode: Optional[PaymentMode] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve expenses with optional filtering
    """
    filters = ExpenseFilter(
        category=category,
        payment_mode=payment_mode,
        start_date=start_date,
        end_date=end_date
    )
    return get_expenses(db=db, user_id=current_user.id, skip=skip, limit=limit, filters=filters)


@router.get("/{expense_id}", response_model=ExpenseResponse)
def read_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific expense by ID
    """
    return get_expense_by_id(db=db, expense_id=expense_id, user_id=current_user.id)


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense_endpoint(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an expense
    """
    return update_expense(db=db, expense_id=expense_id, expense_data=expense_data, user_id=current_user.id)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense_endpoint(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an expense
    """
    delete_expense(db=db, expense_id=expense_id, user_id=current_user.id)
    return None