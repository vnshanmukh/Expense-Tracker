from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date
import calendar

from app.models.expense import Expense, PaymentMode
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseFilter, MonthlySummary, CategorySummary


def create_expense(db: Session, expense_data: ExpenseCreate, user_id: int) -> Expense:
    db_expense = Expense(
        user_id=user_id,
        amount=expense_data.amount,
        category=expense_data.category,
        description=expense_data.description,
        date=expense_data.date,
        payment_mode=expense_data.payment_mode
    )
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    return db_expense


def get_expenses(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100,
    filters: Optional[ExpenseFilter] = None
) -> List[Expense]:
    query = db.query(Expense).filter(Expense.user_id == user_id)
    
    if filters:
        if filters.category:
            query = query.filter(Expense.category == filters.category)
        if filters.payment_mode:
            query = query.filter(Expense.payment_mode == filters.payment_mode)
        if filters.start_date:
            query = query.filter(Expense.date >= filters.start_date)
        if filters.end_date:
            query = query.filter(Expense.date <= filters.end_date)
    
    return query.order_by(Expense.date.desc()).offset(skip).limit(limit).all()


def get_expense_by_id(db: Session, expense_id: int, user_id: int) -> Expense:
    expense = db.query(Expense).filter(
        Expense.id == expense_id, 
        Expense.user_id == user_id
    ).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    return expense


def update_expense(db: Session, expense_id: int, expense_data: ExpenseUpdate, user_id: int) -> Expense:
    expense = get_expense_by_id(db, expense_id, user_id)
    
    update_data = expense_data.dict(exclude_unset=True)
    

    update_data.pop("date", None)

    for key, value in update_data.items():
        setattr(expense, key, value)
    
    db.commit()
    db.refresh(expense)
    
    return expense



def delete_expense(db: Session, expense_id: int, user_id: int) -> None:
    expense = get_expense_by_id(db, expense_id, user_id)
    
    db.delete(expense)
    db.commit()
    
    return None


def get_monthly_summary(db: Session, user_id: int, year: int, month: int) -> MonthlySummary:
    # Validate month and year
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Month must be between 1 and 12"
        )
    
    # Get expenses for the specified month
    expenses = db.query(Expense).filter(
        Expense.user_id == user_id,
        extract('year', Expense.date) == year,
        extract('month', Expense.date) == month
    ).all()
    
    # Calculate summary
    total_amount = sum(expense.amount for expense in expenses)
    
    # Group by category
    category_summary = {}
    for expense in expenses:
        if expense.category not in category_summary:
            category_summary[expense.category] = {
                'total_amount': 0.0,
                'count': 0
            }
        category_summary[expense.category]['total_amount'] += expense.amount
        category_summary[expense.category]['count'] += 1
    
    categories = [
        CategorySummary(
            category=category,
            total_amount=data['total_amount'],
            count=data['count']
        )
        for category, data in category_summary.items()
    ]
    
    return MonthlySummary(
        month=calendar.month_name[month],
        year=year,
        total_amount=total_amount,
        categories=categories
    )


def get_all_expenses_for_export(db: Session, user_id: int) -> List[Expense]:
    return db.query(Expense).filter(Expense.user_id == user_id).order_by(Expense.date.desc()).all()