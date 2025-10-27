from datetime import datetime
from pydantic import BaseModel


class BaseExpenseSchema(BaseModel):
    desc: str
    amount: float


class ExpenseResponseSchema(BaseModel):
    id: int
    user_id: int
    desc: str
    amount: float
    expense_date: datetime
