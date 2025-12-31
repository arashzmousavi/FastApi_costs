from datetime import datetime
from pydantic import BaseModel


class BaseExpenseSchema(BaseModel):
    desc: str
    amount: float


class ExpenseResponseSchema(BaseExpenseSchema):
    id: int
    user_id: int
    expense_date: datetime
