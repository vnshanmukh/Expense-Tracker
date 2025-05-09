from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class PaymentMode(str, Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    APPLE_PAY = "apple_pay"
    OTHER = "other"


class ExpenseBase(BaseModel):
    amount: float = Field(..., gt=0)
    category: str = Field(...)
    description: Optional[str] = None
    date: date
    payment_mode: PaymentMode


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    description: Optional[str] = None
    # date: Optional[date] = None
    payment_mode: Optional[PaymentMode] = None


class ExpenseResponse(ExpenseBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExpenseFilter(BaseModel):
    category: Optional[str] = None
    payment_mode: Optional[PaymentMode] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class CategorySummary(BaseModel):
    category: str
    total_amount: float
    count: int


class MonthlySummary(BaseModel):
    month: str
    year: int
    total_amount: float
    categories: List[CategorySummary]


class ExpenseExport(BaseModel):
    filename: str
    content_type: str
    content: str