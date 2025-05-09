import csv
from io import StringIO
from typing import List
from datetime import datetime

from app.models.expense import Expense


def export_expenses_to_csv(expenses: List[Expense]) -> str:
    """
    Export expenses to CSV format
    Returns a string containing CSV data
    """
    output = StringIO()
    fieldnames = ['id', 'date', 'amount', 'category', 'description', 'payment_mode']
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for expense in expenses:
        writer.writerow({
            'id': expense.id,
            'date': expense.date.strftime('%Y-%m-%d'),
            'amount': expense.amount,
            'category': expense.category,
            'description': expense.description,
            'payment_mode': expense.payment_mode.value
        })
    
    return output.getvalue()


def generate_csv_filename(user_id: int) -> str:
    """
    Generate a filename for the CSV export
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"expenses_user_{user_id}_{timestamp}.csv"