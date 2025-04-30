from typing import Optional

from pydantic import BaseModel


class Expense(BaseModel):
    date: Optional[str] = None
    amount: float
    description: str
    category: str


class ExpenseResponse(BaseModel):
    id: int
    date: str
    amount: float
    description: str
    category: str
