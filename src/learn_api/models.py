from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Expense(BaseModel):
    expense_id: Optional[str] = None
    title: str
    description: str
    amount: float
    spent_on: datetime
    category: str

    class Config:
        schema_extra = {
            "example": {
                "expense_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Rent",
                "description": "Rent of house",
                "amount": 1000,
                "spent_on": "2022-01-01T00:00:00",
            }
        }

"""
Only show certain fields 
"""

class ExpenseResponse(BaseModel):
    title: str
    description: str
    amount: float

    class Config:
        orm_mode = True


