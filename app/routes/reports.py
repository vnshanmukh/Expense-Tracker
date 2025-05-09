from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime
import calendar

from app.database import get_db
from app.schemas.expense import MonthlySummary, ExpenseExport
from app.services.expenses import get_monthly_summary, get_all_expenses_for_export
from app.utils.exporter import export_expenses_to_csv, generate_csv_filename
from app.security.jwt import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/monthly/{year}/{month}", response_model=MonthlySummary)
def get_monthly_expense_summary(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get monthly expense summary grouped by category
    """
    return get_monthly_summary(db=db, user_id=current_user.id, year=year, month=month)


@router.get("/export/csv")
def export_expenses_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Export all expenses as CSV
    """
    expenses = get_all_expenses_for_export(db=db, user_id=current_user.id)
    
    if not expenses:
        return Response(content="No expenses found", media_type="text/plain")
    
    csv_content = export_expenses_to_csv(expenses)
    filename = generate_csv_filename(current_user.id)
    
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers=headers
    )